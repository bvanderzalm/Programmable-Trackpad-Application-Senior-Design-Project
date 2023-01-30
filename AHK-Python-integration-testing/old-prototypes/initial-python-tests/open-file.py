# exec(open("test-script.ahk").read())
# DOESN'T WORK at the moment, would like more testing with this subprocess library though
import subprocess


subprocess.call(["\Program Files\AutoHotkey\AutoHotkey.exe"], "test-script.ahk")