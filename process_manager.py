# version: 0.0.5
# author: picklez

# general imports
import os
import psutil

cpu_process_count = psutil.cpu_count()

# code for arguments in command line
import argparse
parser = argparse.ArgumentParser(description="Valid Arguments for Process list getting", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-ls","--get_PIDs",action="store_true",help="Just returns ProcessID list")
parser.add_argument("-pyls","--get_py_PIDs",action="store_true",help="Just returns ProcessID list for all instances of Python")
parser.add_argument("-nopyls","--get_not_py_PIDs",action="store_true",help="Just returns ProcessID list for all processes that are not Python")
parser.add_argument("-p","--print",action="store_true",help="Will print the arguments asked for")
parser.add_argument("-espy","--escalate_py",action="store_true",help="Will escalate Python processes to realtime (need to be admin to do)")
args = parser.parse_args()
config = vars(args)

def get_PIDs():
    processes = []
    for proc in psutil.process_iter(['pid','name']):
        processes.append(proc.info)
    return processes
    
def get_py_PIDs():
    processes = get_PIDs()
    hold = []
    for item in processes:
        if item['name'] == 'py.exe' or item['name'] == 'python.exe' or item['name'] == 'Python.exe':
            hold.append(item)
    return hold

def get_not_py_PIDs():
    processes = get_PIDs()
    hold = []
    for item in processes:
        if item['name'] != 'py.exe' or item['name'] != 'python.exe' or item['name'] != 'Python.exe':
            hold.append(item)
    return hold

def has_admin():
    import os
    if os.name == 'nt':
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        except:
            return (os.environ['USERNAME'],False)
        else:
            return (os.environ['USERNAME'],True)
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return (os.environ['SUDO_USER'],True)
        else:
            return (os.environ['USERNAME'],False)
            
def has_admin_simply():
    hold = has_admin()
    return hold[1]


# argument operations
if config['escalate_py'] == True:
    if has_admin_simply() == True:
        py_PIDs = get_py_PIDs()
        for ID in py_PIDs:
            process = psutil.Process(ID['pid'])
            process.nice(psutil.REALTIME_PRIORITY_CLASS)
    else:
        print("Can't escalate; do not have admin privileges.")
if config['print'] == True:
    if config['get_PIDs'] == True:
        print("\nEntire ProcessID list:\n"+str(get_PIDs()))
    if config['get_py_PIDs'] == True:
        print("\nProcessID list for just PythonIDs:\n"+str(get_py_PIDs()))
    if config['get_not_py_PIDs'] == True:
        print("\nProcessID list w/ PythonIDs:\n"+str(get_not_py_PIDs()))
