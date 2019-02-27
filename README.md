# Mini Project: Option A 

This is a python wrapper that will run various tools on E coli K-12 reads and produce results in a folder and log file.

The following must be installed if not already:
- SRA-toolkit: https://ncbi.github.io/sra-tools/install_config.html
- python3: https://realpython.com/installing-python/, https://www.python.org/downloads/ (though this should be installed already)  
- SPAdes: http://cab.spbu.ru/software/spades/  
- Prokka: https://github.com/tseemann/prokka  
- TopHat2, Bowtie2, Cufflinks: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3334321/  

All of these tools must be on the same machine. If you don't have the wget command, install that too.  

When prompt to enter a path, include the directory for which you want all the outputs to go into. For example, if I wanted my results to output into a folder called 'Myfolder', I would type in: /Users/Name/Desktop/MyFolder i.e. /path/MyFolder. Where you want the results to be located is up to you.

OptionA.py and sample.txt must also be in the same location/directory. 

## Use:

Run on command line:  
``
python3 optionA.py
``
