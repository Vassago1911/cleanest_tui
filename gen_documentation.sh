sphinx-apidoc -f -o source/ lib/
# sphinx-apidoc -f -o source/ .
# rm source/conf.rst
make clean
make html

# now you can open the _build/index.html in a browser of your choice, like firefox
