#! /usr/bin/python


#
## ls_categorized
#
# Description.
#
# 
#


import subprocess # .call
import tput # .colorize, .decolorize
import sys # .argv


INDENT = '  '
SORT_ORDER = ['-c'] #TODO. Is a list of args to ls that say how to sort (within categories)
C_FILE_EXTENSIONS = ['.c', '.h', '.cpp']
TEXT_FILE_EXTENSIONS = ['.txt'] # TODO add more?
PICTURE_FILE_EXTENSIONS = ['.jpg', '.png', '.gif'] # TODO add more
ARCHIVE_FILE_EXTENSIONS = ['.zip', '.tar', '.gz', '.bz2', '.rar'] # TODO add more
PACKAGE_FILE_EXTENSIONS = ['.app'] # TODO add more?


# allow lsing dirs other than .
# and allow passing other args to the interior 'ls'
args_1 = sys.argv[1:]







### Helper, yo

def extension_in(one, list_of_extensions):
    for extension in list_of_extensions:
        
        nChars = len(extension)
        sliced = one[-nChars:]

        if sliced == extension:
            return True

    return False
# end extension_in

# Another helper, yo
#
# To enable compatibility even on unixes with old versions of python,
# re-implement the python2.7 function subprocess.check_output
def subp_check_output(popen_arg_list):

    # from: http://stackoverflow.com/a/4814985
    return subprocess.Popen(popen_arg_list, stdout=subprocess.PIPE).communicate()[0]
    











### Create ells and ones, yo


# that's a -"ell"
ls_ell_string = subp_check_output(['ls', '-lat'] + SORT_ORDER + args_1)
ls_ell_lines = ls_ell_string.split('\n')

ls_ell_lines = ls_ell_lines[1:] # throw away the "total" line
ls_ell_lines = ls_ell_lines[:-1] # throw away the final blank line

# that's a -"one"
ls_one_string = subp_check_output(['ls', '-1at'] + SORT_ORDER + args_1)
ls_one_lines = ls_one_string.split('\n')
ls_one_lines = ls_one_lines[:-1] # throw away the final blank line










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
# blue for code
# green otherwise
soft_links = Category("SOFT LINKS", "RED")
directories = Category("DIRECTORIES", "RED")
executables = Category("EXECUTABLES", "BLUE")
c_files = Category("[CH]", "BLUE")
texts = Category("TEXTS", "GREEN")
pictures = Category("PICTURES", "GREEN")
packages = Category("PACKAGES", "RED")
archives = Category("ARCHIVES", "RED")
others = Category("OTHERS", "GREEN")

# categorize each file
for (one, ell) in zip(ls_one_lines, ls_ell_lines):
    
    # soft link?
    if ell[0] == 'l':
        # for soft links, the list entry shall
        # include the -> dest
        arrow_loc = ell.find('->')
        arrow_and_dest = ell[arrow_loc:]
        soft_links.addItem(one + ' ' + arrow_and_dest)
	continue

    # directory?
    # // includes dotdirs
    if ell[0] == 'd':
	directories.addItem(one)
	continue

    # executable?
    # current method of checking:
    #  is executable to owner?
    if ell[3] == 'x':
	executables.addItem(one)
	continue

    # c_file?
    if extension_in(one, C_FILE_EXTENSIONS):
        c_files.addItem(one)
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

PRINTING_ORDER = [soft_links, directories, packages, archives, others, pictures, texts, c_files, executables]


for category in PRINTING_ORDER:
    if len(category.items) > 0:
    
        print ''

        tput.colorize(fg = category.color, bold = True)
        print INDENT, category.name
        tput.decolorize()

        for one in category.items:
            print INDENT, one

# done-zo-matic

