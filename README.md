DBLPbib
=======

This is a tiny python script to download bibtex entries from [DBLP](http://dblp.uni-trier.de/) automatically.
It searches the contents of a list of tex files for citations whose bibtex entry is not in a given database yet, downloads the missing entries, and adds them to the database automatically

Howto
=====

Suppose you use `paper.bib` for your bibliography and have the contents of your paper in files `intro.tex` and `main.tex`.
Now you want to cite some papers that are not in your bibliography yet.
Suppose you want to cite Donald Knuth's famous LR parsing paper:

Donald E. Knuth: *On the Translation of Languages from Left to Right.* Information and Control 8(6): 607-639 (1965)

You proceed as follows:

1. In his [DBLP entry](http://dblp.uni-trier.de/pers/hd/k/Knuth:Donald_E=), find the paper's dblp key: `journals/iandc/Knuth65` by hovering over the 'arrow down' download symbol.
2. Now, just add `\cite{DBLP:journals/iandc/Knuth65}` to your text, for example in `main.tex`.
3. To update your bibliography, just run
```
$ ./dblpbib.py -o paper.bib intro.tex main.tex
```

Notes
=====

DBLPbib will never erase or modify existing bibtex entries in the specified bibliography.
It will only append missing entries that it downloaded from DBLP.
