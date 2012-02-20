

"""
dirty rotten hack to make subprocess.check_output work on python2.6 (rescomp)
"""


from subprocess import *


try:
    check_output # test if it exists
except:
    
    def check_output(popen_arg_list):
        
        # from: http://stackoverflow.com/a/4814985
        return Popen(popen_arg_list, stdout=PIPE).communicate()[0]
    

