import psutil
import os

process_name = "vServer"
pid = None

for proc in psutil.process_iter():
    if process_name in proc.name():
       pid = proc.pid
       break

print("Pid:", pid)
