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



