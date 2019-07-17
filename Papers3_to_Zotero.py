#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script takes as input a BibTeX library exported from readcube/mekentosj Papers3 and outputs a BibTex library for Zotero to import.
The script preserves your Papers citekeys, adds supplementary files from the Papers3 Library, removes duplicate links to PDFs and removes extraneous *.html and *.webarchive files that are often created by importing articles into Paper from a web browser.

__Instructions for use__:

* Make sure to have Better BibTeX pre-installed to Zotero if you want to preserve the Papers citekeys.

* Export your Papers3 library as a *.bib file.
    Export > BibTeX Library
    Make sure to set the “BibTex Record” option to “Complete”. This will cause papers to include the paths to the main PDF (or whatever) file in the *.bib export

* In this script, update the ‘papers_library’ and ‘bibtex_library’ variables with the paths to your Papers3 library and the BibTeX library that you just exported.
    e.g.
    bibtex_library = Path(“~/Desktop/full_library_export.bib") ### Path to Papers BibTex library export
    papers_library = Path(“~/Documents/user’s Library/Library.papers3") ### Path to Papers3 Library

* Run this script with python 3.5 or higher

* Import the 'zotero_import.bib’ file that gets generated with Zotero.

* Be sure to check the 'Import errors found:' file if Zotero generates one (if it exists, it will be in whatever folder you imported the library to; sort by title to find it).

__NOTE__:
The Collections groupings are not preserved with this method. This is one way to manually get your Papers3 Collections into Zotero after following the above instructions:

* Export each collection as a BibTex library (“Export” set to “Selected Collection” and “BibTex Record” set to “Standard”). This will prevent any file paths from being included in the *.bib file.

* Import that *.bib file directly to Zotero with the option to “Place imported collections and items into new collection” selected.

* Then merge the duplicate records. That will give you a new collection with links to right papers from your Zotero library.

* In this strategy, you have to do that for each one of your Papers3 Collections. Not ideal but maybe tolerable.
"""

from pathlib import Path
import re

### Update these paths:
bibtex_library = Path("~/Desktop/library.bib").expanduser() ### Path to Papers BibTeX library export
papers_library = Path("~/Documents/daeda's Library/Library.papers3").expanduser() ### Path to Papers3 Library


out = list()
papers_library_string = str(papers_library) + '/'

if papers_library_string[-9:] != '.papers3/':
    raise Exception(f'The variable \'papers_library\' should end in with \'.papers3\' but is rather: \n\t{str(papers_library)}')
if not papers_library.exists():
    raise Exception(f'The path you provided to the Papers3 library does not seem to exist: \n\t{str(papers_library)}')
if not bibtex_library.exists() and bibtex_library.is_file() and bibtex_library.suffix == '.bib':
    raise Exception(f'The path you provided to the BibTex Library file you exported from Papers3 does not seem to exist or is not \'.bib\' file: \n\t{str(bibtex_library)}') 

with open(bibtex_library, 'r') as btlib:
    for line in btlib:
        if line.startswith('file = {'):
            templine = re.sub(r'^file = {{(.*?)}},?', r'file = {\1},', line, flags = re.M)
            newline = re.sub(r'^file = {(.*?);(\1)},?', r'file = {\1},', templine, flags = re.M)
            
            assert ';' not in newline ### assert there is only one file
            
            result = re.search(r"^file = {.*?:" + papers_library_string + r"(.*?)\.(.*?):(.*?/.*?)},?", newline)

            primary_file_path = Path(papers_library_string) / Path(result.group(1)).with_suffix('.'+result.group(2))
            
            supp_files = list()
            for dir_extra in ['Supplemental', 'Media']:
                supp_dir = primary_file_path.parents[0] / dir_extra
                if supp_dir.exists():
                    for x in supp_dir.iterdir():
                        if x.is_file() and x.suffix not in ['.html', '.webarchive'] and str(x) != str(primary_file_path):
                            supp_files.append(x)
                    
                    if len(supp_files) > 0:
                        primary_line = re.search(r"(^file = {.*?:" + papers_library_string + r".*?\..*?:application/.*?)},?", newline)
                        newline = primary_line.group(1)
                        for x in supp_files:
                            print(f'adding supplementary file for {x.name}')
                            newline += f';{x.with_suffix("").name + " Supp" + x.suffix}:{x}:application/{x.suffix}'
                        newline += '},\n'
            out.append(newline)
        else:
            out.append(line)


### New BibTeX record to import into Zotero
modified_lib = bibtex_library.parents[0] / 'zotero_import.bib'
with open(modified_lib, 'w') as outfile:
    for item in out:
        outfile.write(item)

print(f'\n\nScript appears to have completed successfully. You can now import this file into Zotero (make sure Better BibTeX is already installed): \n\t{str(modified_lib)}')
