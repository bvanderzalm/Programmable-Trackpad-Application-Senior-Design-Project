import subprocess, os

currentPath = os.getcwd() + '\\test-script.exe'
# print(currentPath)

subprocess.Popen(currentPath)
