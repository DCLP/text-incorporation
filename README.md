Tools for incorporating DCLP texts into existing XML files
===========================================================

Step 1
-------
Use ```scripts/regularize-file-names.py``` to copy Würzburg-style files into filenames that look like we expect (i.e., that only put the idno in the filename, plus "xml" as extension):

```
	$ python scripts/regularize-file-names.py -h
	usage: regularize-file-names.py [-h] [-l LOGLEVEL] [-v] [-vv] indir outdir
	
	regularize filenames
	
	positional arguments:
	  indir                 input directory path
	  outdir                output directory path
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -l LOGLEVEL, --loglevel LOGLEVEL
	                        desired logging level (case-insensitive string: DEBUG,
	                        INFO, WARNING, ERROR (default: None)
	  -v, --verbose         verbose output (logging level == INFO (default: False)
	  -vv, --veryverbose    very verbose output (logging level == DEBUG (default:
	                        False)
```

Verify you get clean output, i.e., XML filenames that are only of the form ```\d+\.xml``` and that the numeric portions of these filenames match internal ```<idno type="TM">``` text node values.

Step 2
-------
Execute ```scripts/incorporate_texts.py``` in order to incorporate the text contents of same into the proper metadata xml files. 

```
	$ python scripts/incorporate_texts.py -h
	usage: incorporate_texts.py [-h] [-l LOGLEVEL] [-v] [-vv] -c CANDIDATES -m
	                            METADIR -e EDITIONDIR -o OUTPUTDIR -w WHO [-x]
	
	run a series of EpiDoc edition div incorporation transforms
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -l LOGLEVEL, --loglevel LOGLEVEL
	                        desired logging level (case-insensitive string: DEBUG,
	                        INFO, WARNING, ERROR (default: None)
	  -v, --verbose         verbose output (logging level == INFO (default: False)
	  -vv, --veryverbose    very verbose output (logging level == DEBUG (default:
	                        False)
	  -c CANDIDATES, --candidates CANDIDATES
	                        path to text file containing a list of TM numbers to
	                        try to operate on (default: None)
	  -m METADIR, --metadir METADIR
	                        path to directory containing metadata XML files
	                        (default: None)
	  -e EDITIONDIR, --editiondir EDITIONDIR
	                        path to directory containing edition division files
	                        (default: None)
	  -o OUTPUTDIR, --outputdir OUTPUTDIR
	                        path to directory in which to output results (default:
	                        None)
	  -w WHO, --who WHO     Name of person to be credited in the revision
	                        description for running this script (default: None)
	  -x, --overwrite       overwrite existing edition divs (default: False)
```

