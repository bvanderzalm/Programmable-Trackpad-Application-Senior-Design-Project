# This file is attempting to stop through command, successful 
# only if python program is terminated and then type in custom ahk command 'exitahk'
import os

print('this runs')

path = "our-project-program-files/Exe-files/"
os.chdir(path)
os.system("script-with-exit-cmd.exe")

print('this does not run unless AHK is terminated manually')

exit = input('Type yes to exit:\n')
print(exit)
if exit == 'yes':
    os.system("exitahk")


