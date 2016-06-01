# Makefile for pushing our files to git

clean:
	rm -f *~ .*.*.*~ .*.*.swo .*.*.swp

osx:
    buildozer osx debug

ios:
    buildozer ios debug

