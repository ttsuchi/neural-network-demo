# 2015 ERSP Project: Neural Network Tutorial
A demonstration of how a neural network trains and make predictions.

### Project Goals:
 * To (re)create the neural network demo code in Python
 * Improve the user interface by using the kivy toolkit
 * Add ways to visualize network activations

### Installation (for developers):
Download kivy and follow the instructions from [here](https://kivy.org/#download).  Make sure you are able to perform
 
```bash
kivy src/main.py
```

### Building for iOS

```
.buildozer/ios/platform/kivy-ios
./toolchain.py build kivy
buildozer ios debug
```

Also follow the instructions from [here](https://github.com/kivy/kivy-ios/pull/108) to compile numpy.