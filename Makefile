# Makefile for pushing our files to git

git:
	rm -f *~ .*.*.*~ .*.*.swo .*.*.swp
	git rm -r --cached .
	git add .
	git commit -m "No commit message"
	git push
