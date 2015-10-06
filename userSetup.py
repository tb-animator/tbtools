# Put this file in your user scripts folder so it gets executed automatically when maya starts. 
# In case you already have a userSetup.py file, just copy the following line into it.
# Note: Below path is just an example, and of course, you can put the Ritalin script files in any other folder you see fit. 
# In any way you need to change the following path according to the actual folder you copied the files to.
print "****************************************************************"
print "\t\ttb-tools module loading\n"
print "****************************************************************"

import tb_hotKeys as tb_hotKeys
tb_hotKeys.add_tbtools_commands()
