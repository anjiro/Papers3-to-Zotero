# coding: utf-8

#####
# This script uses the BibTeX export from Papers 3 (with the BibTeX Record set to 'Compelte' such that file paths are included)
# and searches for supplimentrary materials from those publications, and removes duplicate files that Papers includes.
# Make sure to have Better BibTeX pre-installed if you want to preserve the Papers citekeys.
# The Collections groupings are not preserved, if you use this script to import your full library, then export each Collection with
# the BibTeX Record set to 'Minimal', you can import each of these to Zotero, then merge the duplicate records without duplicating files.
#####

from pathlib import Path
import re

### Update these paths
bibtex_library = Path("/Volumes/cristae/samadhi_daeda/Desktop/paperlib/full.bib") ### Path to Papers BibTex library export
papers_library_string = "/Users/daeda/Documents/daeda's Library/Library.papers3/" ### requires terminal '/'

out = list()
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
                            print(x.name)
                            newline += f';{x.with_suffix("").name + " Supp" + x.suffix}:{x}:application/{x.suffix}'
                        newline += '},\n'
            out.append(newline)
        else:
            out.append(line)


### New BibTeX record to import into Zotero
with open(bibtex_library.parents[0] / 'zotero_import.bib', 'w') as outfile:
    for item in out:
        outfile.write(item)