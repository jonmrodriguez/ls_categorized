#! /usr/bin/python


#
## ls_categorized
#
# Description.
#
# 
#


import subprocess # .call and .check_output
import tput # .colorize, .decolorize


SORT_ORDER = ['-c'] #TODO. Is a list of args to ls that say how to sort (within categories)
TEXT_FILE_EXTENSIONS = ['.txt'] # TODO add more?
PICTURE_FILE_EXTENSIONS = ['.jpg', '.png', '.gif'] # TODO add more
ARCHIVE_FILE_EXTENSIONS = ['.zip', '.tar', '.gz', '.bz2'] # TODO add more
PACKAGE_FILE_EXTENSIONS = ['.app'] # TODO add more?


# that's a -"ell"
ls_ell_string = subprocess.check_output(['ls', '-lt'] + SORT_ORDER)
ls_ell_lines = ls_ell_string.split('\n')

ls_ell_lines = ls_ell_lines[1:] # throw away the "total" line
ls_ell_lines = ls_ell_lines[:-1] # throw away the final blank line

# that's a -"one"
ls_one_string = subprocess.check_output(['ls', '-1t'] + SORT_ORDER)
ls_one_lines = ls_one_string.split('\n')
ls_one_lines = ls_one_lines[:-1] # throw away the final blank line


### Helper, yo

def extension_in(one, list_of_extensions):
    for extension in list_of_extensions:
        
        nChars = len(extension)
        sliced = one[-nChars:]

        if sliced == extension:
            return True

    return False
# end extension_in


### Categorize shit, yo

class Category():
    def __init__(self, name, color):
        self.items = []
        self.name = name
        self.color = color

    def addItem(self, item):
        self.items += [item]

# check membership in this order. membership := the first one that's true
# red for containers
# magenta for executables
# green otherwise
soft_links = Category("SOFT LINKS", "GREEN")
directories = Category("DIRECTORIES", "RED")
executables = Category("EXECUTABLES", "MAGENTA")
texts = Category("TEXTS", "GREEN")
pictures = Category("PICTURES", "GREEN")
packages = Category("PACKAGES", "RED")
archives = Category("ARCHIVES", "RED")
others = Category("OTHERS", "GREEN")

# categorize each file
for (one, ell) in zip(ls_one_lines, ls_ell_lines):
    
    # soft link?
    if ell[0] == 'l':
        soft_links.addItem(one)
	continue

    # directory?
    if ell[0] == 'd':
	directories.addItem(one)
	continue

    # executable?
    # current method of checking:
    #  is executable to owner?
    if ell[3] == 'x':
	executables.addItem(one)
	continue

    # text?
    if extension_in(one, TEXT_FILE_EXTENSIONS):
	texts.addItem(one)
	continue

    # picture?
    if extension_in(one, PICTURE_FILE_EXTENSIONS):
	pictures.addItem(one)
	continue

    # package?
    if extension_in(one, PACKAGE_FILE_EXTENSIONS):
	packages.addItem(one)
	continue

    # archive?
    if extension_in(one, ARCHIVE_FILE_EXTENSIONS):
	archives.addItem(one)
	continue

    # other.
    others.addItem(one)
    continue

# end for


### Print shit, yo

PRINTING_ORDER = [soft_links, directories, packages, archives, others, pictures, texts, executables]


for category in PRINTING_ORDER:
    if len(category.items) > 0:
    
        print ''

        tput.colorize(fg = category.color, bold = True)
        print category.name
        tput.decolorize()

        for one in category.items:
            print one

# done-zo-matic

