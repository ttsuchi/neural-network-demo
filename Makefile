# Makefile for pushing our files to git

clean:
	rm -f *~ .*.*.*~ .*.*.swo .*.*.swp

osx:
    buildozer osx debug

ios:
	cd .buildozer/ios/platform/kivy-ios
	./toolchain.py build kivy
    buildozer ios debug

