import time
from ahk import AHK, Hotkey
ahk = AHK()

# ahk_script = 'Run Notepad'
# ahk.run_script(ahk_script, blocking=False)

key_combo = 'F4'
script = 'Run Notepad'
hotkey = Hotkey(ahk, key_combo, script)
hotkey.start()

exit = input('Press any key to exit\n')
print(exit)