from numpy import *
from numpy.linalg import pinv
from numpy.linalg import svd
from numpy.random import permutation
from numpy.random import random_sample


def _onehot_encode(y):
    C = unique(y)
    N = len(y)
    Y = zeros((N, len(C)))
    Y[arange(N), y] = 1.0
    return Y


def _train_test_split(X, T, test_size=0.25):
    N = len(T)
    S = floor(N * test_size)
    idx = permutation(N)
    idx_test = zeros(N, dtype=bool)
    idx_test[idx[:S]] = True
    return X[idx[S:]], X[idx[:S]], T[idx[S:]], T[idx[:S]], idx_test


class ShuffleSplit(object):
    """Base class for ShuffleSplit and StratifiedShuffleSplit"""

    def __init__(self, n, n_iter=10, test_size=0.1, train_size=None,
                 random_state=None):
        self.n = n
        self.n_iter = n_iter
        self.test_size = test_size
        self.train_size = train_size
        self.random_state = random_state
        self.n_test = int(floor(n * test_size))
        self.n_train = n - self.n_test

    def __iter__(self):
        for i in range(self.n_iter):
            # random partition
            permutation = permutation(self.n)
            ind_test = permutation[:self.n_test]
            ind_train = permutation[self.n_test:self.n_test + self.n_train]
            yield ind_train, ind_test


class PCAData(object):
    def __init__(self, data):
        X = data.copy()
        self.mean_ = X.mean(axis=0)
        X -= self.mean_
        U, S, V = svd(X, full_matrices=False)
        self.V = V
        self.explained_variance_ = ((S ** 2) / X.shape[0])

    @property
    def explained_variance(self):
        return self.explained_variance_ / self.explained_variance_.sum()


class PCATransformer(object):
    def __init__(self, pca_data, pca_components):
        self.mean_ = pca_data.mean_
        self.V = pca_data.V[:int(pca_components)]
        self.explained_variance_ = pca_data.explained_variance_[:int(pca_components)]

    def transform(self, X):
        return dot(X - self.mean_, self.V.T) / sqrt(self.explained_variance_)

    def inverse_transform(self, Xt):
        return dot(Xt * sqrt(self.explained_variance_), self.V) + self.mean_

    def reconstruct(self, X):
        image_shape = X.shape
        return self.inverse_transform(self.transform(X.flatten())).reshape(image_shape)


class NeuralNetwork(object):
    def __init__(self, app):
        self.app = app

    def reset_training(self):
        """Initialize the network for training."""
        app = self.app
        self.targets = app.dataset[app.target_name] - 1

        target_code_name = app.target_name + '_Code'
        if app.dataset.has_key(target_code_name):
            self.target_names = app.dataset[target_code_name]
        else:
            self.target_names = dict([(t + 1, str(t + 1)) for t in unique(self.targets)])

        self.n_output = len(unique(self.targets))
        self.V_hidden = zeros((int(app.pca_components) + 1, app.num_hidden_units))
        self.W_hidden = random_sample(self.V_hidden.shape)
        self.V_output = zeros((app.num_hidden_units + 1, self.n_output))
        self.W_output = random_sample(self.V_output.shape)

        self.hidden_units_learning_rate = app.hidden_units_learning_rate
        self.output_units_learning_rate = app.output_units_learning_rate

        self.X = X = app.dataset['data']
        # Split into training and test
        X_train, X_test, self.y_train, self.y_test, self.idx_test = \
            _train_test_split(X, self.targets, test_size=app.num_test_data)

        # Preprocess the data using PCA
        self.pca_transformer = PCATransformer(PCAData(X_train), int(app.pca_components))
        self.X_train = self.pca_transformer.transform(X_train)
        self.X_test = self.pca_transformer.transform(X_test)

        # Epochs
        self.epoch = 0
        self.minimum_rmse = app.minimum_rmse
        if self.minimum_rmse > 0:
            # Use Training RMSE to stop
            self.should_keep_training = lambda: self.rmse[self.epoch, 1] > app.minimum_rmse
            self.rmse = zeros((0, 2))
            self.cerr = zeros((0, 2))
        else:
            # Use epochs to stop
            self.should_keep_training = lambda: self.epoch < app.epochs
            self.rmse = zeros((app.epochs, 2))
            self.cerr = zeros((app.epochs, 2))

    def resume_training(self):
        """Resume training the network"""
        while self.should_keep_training():
            # Test then Train, since we'll use the training errors
            for i, (inputs, y) in enumerate([[self.X_test, self.y_test], [self.X_train, self.y_train]]):
                outputs, hidden = self.feed_forward(inputs)
                target = ones(outputs.shape) * (-1.0)
                target[arange(target.shape[0]), y] = 1.0
                errors = target - outputs
                self.rmse[self.epoch, i] = sqrt((errors ** 2).mean())  # RMSE
                self.cerr[self.epoch, i] = (y != argmax(outputs, axis=1)).mean()

            # Yield the results to outside
            yield self.epoch, self.rmse.shape[0], self.rmse[:self.epoch], self.cerr[:self.epoch], False

            # Update weights using backpropagation
            self.back_propagate(inputs, hidden, outputs, errors)

            self.epoch += 1

        # Do once more for the very last epoch
        yield self.epoch, self.rmse.shape[0], self.rmse[:self.epoch], self.cerr[:self.epoch], True

    def _activation(self, x):
        """ Funny tanh function. """
        z = x * 2 / 3
        y = (exp(z) - exp(-z)) / (exp(z) + exp(-z))
        return 1.7159 * y

    def _da(self, x):
        return (1.7159 - multiply(x, x) / 1.7159) * 2 / 3

    def _inverse_activation(self, x):
        z = x / 1.7159
        return z
        # z[z<-.999] = -.999; z[z>.999] = .999
        # return arctanh(z)*3/2

    def feed_forward(self, X):
        """From the input X, calculate the activations at the hidden layer and the output layer."""
        Z = self._activation(dot(c_[X, ones((X.shape[0], 1))], self.W_hidden))
        return self._activation(dot(c_[Z, ones((X.shape[0], 1))], self.W_output)), Z

    def back_propagate(self, inputs, hidden, output, errors):
        """Back-propagate the errors and update the weights."""
        d_output = self._da(output) * errors
        d_hidden = self._da(hidden) * dot(d_output, self.W_output[:-1].T)

        n_samples = inputs.shape[0]
        bias = ones((n_samples, 1))
        # Update momentum and weights
        self.V_output = self.output_units_learning_rate * dot(c_[hidden, bias].T, d_output) / n_samples
        self.W_output += self.V_output

        self.V_hidden = self.hidden_units_learning_rate * dot(c_[inputs, bias].T, d_hidden) / n_samples
        self.W_hidden += self.V_hidden

    def predict_all(self):
        """Returns the predictions and the reconstructions for all training / test data."""
        outputs, hidden = self.feed_forward(self.pca_transformer.transform(self.X))
        hidden_expected = dot(self._inverse_activation(outputs), pinv(self.W_output))[:, :-1]
        hidden_reconstruction = self.pca_transformer.inverse_transform(
            dot(self._inverse_activation(hidden_expected), pinv(self.W_hidden))[:, :-1])
        return outputs.argmax(axis=1), hidden_reconstruction.reshape(self.app.dataset['images'].shape)
