print "****************************************************************"
print "\t\ttb-tools module loading\n"
print "****************************************************************"

import tb_keyCommands as tb_hotKeys
reload(tb_hotKeys)
tb_hotKeys.hotkey_tool().update_commands()
tb_hotKeys.hotkey_tool().remove_bad_commands()

# testing something
