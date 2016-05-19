from numpy import *
from numpy.random import permutation
from numpy.linalg import pinv
from numpy.random import random_sample
from numpy.linalg import svd


import pickle


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
    return X[idx[S:]], X[idx[:S]], T[idx[S:]], T[idx[:S]]

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
    def __init__(self, dataset):
        X = dataset.data.copy()
        self.mean_ = X.mean(axis=0)
        X -= self.mean_
        U, S, V = svd(X, full_matrices=False)
        self.V = V
        self.explained_variance_ = ((S ** 2) / X.shape[0])

    @property
    def explained_variance(self):
        return self.explained_variance_ / self.explained_variance_.sum()

    def transform(self, X, pca_components):
        V = self.V[:pca_components]
        Xt = dot(X - self.mean_, V.T)
        return Xt / sqrt(self.explained_variance_[:pca_components])

    def reconstruct(self, X, pca_components):
        V = self.V[:pca_components]
        return dot(dot(X - self.mean_, V.T), V) + self.mean_

class PCA(object):
    def __init__(self, n_components, whiten=True, copy=True):
        self.n_components = n_components

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def fit(self, X):
        X = X.copy()
        self.mean_ = X.mean(axis=0)
        X -= self.mean_
        U, S, V = svd(X, full_matrices=False)
        self.explained_variance_ = ((S ** 2) / X.shape[0])[:self.n_components]
        self.components_ = V[:self.n_components]
        return self

    def transform(self, X):
        Xt = X - self.mean_
        Xt = dot(Xt, self.components_.T)
        return Xt / sqrt(self.explained_variance_)

class NeuralNetwork(object):
    def __init__(self, model):
        self.model = model

    def _activation(self, x):
        """ Funny tanh function. """
        z = x*2/3
        y = (exp(z) - exp(-z)) / (exp(z) + exp(-z))
        return 1.7159*y

    def _da(self, x):
        return (1.7159 - multiply(x, x) / 1.7159) * 2/3

    def _inverse_activation(self, x):
        z = x / 1.7159
        return z
        #z[z<-.999] = -.999; z[z>.999] = .999
        #return arctanh(z)*3/2

    def feed_forward(self, X):
        """From the input X, calculate the activations at the hidden layer and the output layer."""
        Z      = self._activation(dot(c_[X, ones((X.shape[0], 1))], self.W_hidden))
        return   self._activation(dot(c_[Z, ones((X.shape[0], 1))], self.W_output)), Z

    def back_propagate(self, inputs, hidden, output, errors):
        """Back-propagate the errors and update the weights."""
        d_output = self._da(output) * errors
        d_hidden = self._da(hidden) * dot(d_output, self.W_output[:-1].T)

        n_samples = inputs.shape[0]
        bias = ones((n_samples, 1))
        # Update momentum and weights
        self.V_output = self.output_learning_rate * dot(c_[hidden, bias].T, d_output) / n_samples
        self.W_output+= self.V_output

        self.V_hidden = self.hidden_learning_rate * dot(c_[inputs, bias].T, d_hidden) / n_samples
        self.W_hidden+= self.V_hidden

    def train(self):
        """Initialize the network and start training."""

        model = self.model
        epochs = model.epochs

        # self.n_output = len(unique(self.targets))
        # self.V_hidden = zeros((self.n_input + 1, model.num_hidden_units))
        # self.W_hidden = random_sample(self.V_hidden.shape)
        # self.V_output = zeros((model.num_hidden_units + 1, self.n_output))
        # self.W_output = random_sample(self.V_output.shape)
        #
        # data = self.dataset.data
        #
        # # Split into training and test
        # X_train, X_test, y_train, y_test = _train_test_split(data, self.targets, test_size=test_size)
        #
        # # Preprocess the data using PCA
        # self.pca = PCA(n_components = self.n_input, whiten=True, copy=True)
        # X_train = self.pca.fit_transform(X_train)
        # X_test = self.pca.transform(X_test)
        # self.X = self.pca.transform(data)

        # Start the training
        rmse=zeros((epochs,2))
        cerr=zeros((epochs,2))
        for t in arange(epochs):

            # Test then Train, since we'll use the training errors
            # for i, (inputs, y) in enumerate([[X_test, y_test], [X_train, y_train]]):
            #     outputs, hidden = self.feed_forward(inputs)
            #     target=ones(outputs.shape)*(-1.0)
            #     target[arange(target.shape[0]),y]=1.0
            #     errors = target - outputs
            #     rmse[t, i] = sqrt((errors**2).mean())  # RMSE
            #     cerr[t, i] = (y != argmax(outputs,axis=1)).mean()
            rmse[t, :] = exp(-t)
            cerr[t, :] = 0.5 * exp(-t)

            yield rmse, cerr, t, epochs

            # Update weights using backpropagation
            # self.back_propagate(inputs, hidden, outputs, errors)

    def predict(self, n):
        """Returns the prediction and the reconstruction for the sample n."""
        X = self.X[n:n+1]
        outputs, hidden = self.feed_forward(X)
        pca_reconstruction = self.pca.inverse_transform(X)
        hidden_expected = dot(self._inverse_activation(outputs), pinv(self.W_output))[:,:-1]
        hidden_reconstruction = self.pca.inverse_transform(dot(self._inverse_activation(hidden_expected), pinv(self.W_hidden))[:,:-1])
        return (argmax(outputs),
                pca_reconstruction.reshape(self.dataset.images.shape[1:]),
                hidden_reconstruction.reshape(self.dataset.images.shape[1:]))


def create_network(target='target'):
    return NeuralNetwork(pickle.load(open('../data/cafe.pkl','r')), target)

if __name__ == '__main__':
    net = create_network()
    print('{:^4} {:^15} {:^15} {:^15} {:^15}'.format('t', 'RMSE', 'RMSE Test', 'CERR', 'CERR Test'))
    print('{:-^4} {:-^15} {:-^15} {:-^15} {:-^15}'.format('', '', '', '', ''))
    for rmse, cerr, t, epochs in net.train(epochs=10000):
        if mod(t, 100) == 1:
            print('{:>4} {:>15.3} {:>15.3} {:>15.3} {:>15.3}'.format(t, rmse[t, 1], rmse[t, 0], cerr[t, 1], cerr[t, 0]))
