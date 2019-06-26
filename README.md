# DOI2BIB

Async script to build a BibTeX database out of reference identifiers, including:
    - DOI (Digital Object Identifier)
    - arXiv ID

## Usage

Simply add the DOIs or other supported identifiers to the command line arguments:

    python doi2bib.py id1 id2 id3

You can also create file with line-separated identifiers and use it like this:

    python doi2bib.py -f identifiers.txt

If you want, you can combine both approaches as well:

    python doi2bib.py -f identifiers.txt id1 id2 id3

All identifiers will be collected and duplicates will be omitted.

## Examples

This command:

    $ python doi2bib.py 1510.01797 10.1063/1.467176 10.1021/acs.jctc.5b00784

will create a timestamped file with the following contents:

```bibtex
@article{Chodera_2016,
	doi = {10.1021/acs.jctc.5b00784},
	url = {https://doi.org/10.1021%2Facs.jctc.5b00784},
	year = 2016,
	month = {mar},
	publisher = {American Chemical Society ({ACS})},
	volume = {12},
	number = {4},
	pages = {1799--1805},
	author = {John D. Chodera},
	title = {A Simple Method for Automated Equilibration Detection in Molecular Simulations},
	journal = {Journal of Chemical Theory and Computation}
}
@article{Cao_1994,
	doi = {10.1063/1.467176},
	url = {https://doi.org/10.1063%2F1.467176},
	year = 1994,
	month = {apr},
	publisher = {{AIP} Publishing},
	volume = {100},
	number = {7},
	pages = {5106--5117},
	author = {Jianshu Cao and Gregory A. Voth},
	title = {The formulation of quantum statistical mechanics based on the Feynman path centroid density. {II}. Dynamical properties},
	journal = {The Journal of Chemical Physics}
}
@article{1510.01797,
    Author = {Hans-E. Porst and Ross Street},
    Title = {Generalizations of the Sweedler dual},
    Year = 2015,
    Eprint = {arXiv:1510.01797},
    Doi = {10.1007/s10485-016-9450-2},
}
```

# Disclaimer

This script was only an excuse to play with Python `async` stuff. If you need something like this, you might want to check the [`bibcure` project](https://github.com/bibcure/bibcure).