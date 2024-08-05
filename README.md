# Kurucz-Atoms

This repository holds the Kurucz Atomic database files, which are reformatted into Exomol's .states and .trans files.

Due to the size Limitation, the files cannot be uploaded directly to the GitHub page. Therefore, the data are uploaded to Zenodo and the link will be provided here.


Zenodo Link: https://doi.org/10.5281/zenodo.12819622

The data folder is formatted as: Kurucz/(Atom-name)(_p)/(Atom-name)(_p)/Kurucz/...
Pyexocross requires this folder format to run. Therefore, users could run these files directly within Pyexocross.

Each data is named in the format of (Atom-name)__Kurucz.states/.trans/.pf

The Python files' functionalities:

**CreateFolder.py**: Create all the neutral and singly-charged ion folders in the correct format.  
**FileLineCount.py**: Calculate the number of lines within .states and .trans files by giving the atom names.  
**GrabKuruczAtomic.py**: Scrape files from the Kurucz Atomic Database by giving the website link. GAM, Life, Lines, AGAFGF and pf have different scraping methods. (For Nb I, Tc I, Ru II, Rh I, the agafgf-gz files must be downloaded manually and then processed.)  
**PF_Plot.py**: Plot the partition function based on the given atom names.  
**PF_Process.py**: Process the scraped partition function files and reformat them into the Exomol data structure.  
**Spectra Process.py**: Turn the Pyexocross generated spectra (in wavenumber) to wavelength and then plot them out.  
**States_Merge.py**: Merge those atoms with multiple state(suffix y, w, z) files into one. (Na I, K I, Zn I, Ca II, Y II.)  
**States_Process.py**: Process the scraped states-related files and reformat them into the Exomol data structure.  
**Trans_Merge.py**: Merge those atoms with multiple transition lines(suffix y, w, z) files into one. (Na I, K I, Zn I, Ca II, Y II.)  
**Trans_Process.py**: Process the scraped trans-related files and reformat them into the Exomol data structure.   
**Trans_Remove.py**: Remove the transition lines that either do not have an A coefficient/wavenumber or do not map to any existing states.  

# How to scrape the data
The Kurucz atomic database's website is: http://kurucz.harvard.edu/atoms.html  
To access each atom-related file, find xxyy at the bottom of the webpage, where xx means the element number and yy means neutral when yy = 00 or singly charged when
yy = 01.  
Use **GrabKuruczAtomic.py** to scrape the file by giving the website link.  
Remember to remove the redundant header and match table after scraping the .gam and lifetime files.   
Use **States_Process.py, Trans_Process.py and PF_Process.py** to process each scraped file into Exomol format. (Remember to change atom's name. Match table is needed in State processing.)  
For some atoms, use **States_Merge.py and Trans_Merge.py** to combine them.  
Finally, remove invalid transition lines with **Trans_Remove.py**
