import ctypes
import sys
import subprocess
import socket


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    try:
        with open('configure.bat', 'r') as f:
            data = f.read()

        st = data.index('\\\\') + 2
        end = data[st:].index('\\')
        data = data.replace(data[st:st + end], socket.gethostname())

        with open('configure.bat', 'w') as f:
            f.write(data)

        subprocess.call(['configure.bat'])
        subprocess.call(['python', 'sniffSMB.py', '-p', 'T:'])
    except WindowsError as e:
        pass
    except subprocess.CalledProcessError as e:
        pass

else:
    ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
