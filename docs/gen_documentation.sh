gen_doc() {
    sphinx-apidoc -f -o ./source/ ../lib/
    sphinx-apidoc -f -o ./source/ ../
    rm source/modules.rst
    make clean
    make html
    sphinx-build -b singlehtml . _build/singlehtml
}

gen_doc 1&> doc.log 2&> doc.log

# now you can open the _build/index.html in a browser of your choice, like firefox
got_warnings=0
if [ $(grep WARNING doc.log | wc -l) -lt 1 ]; then got_warnings=0; else got_warnings=1; fi

if [ "$got_warnings" -lt 1 ]; then rm doc.log; rm -r source/; mv _build/singlehtml ../html_docs; rm -r _build/; clear; fi
