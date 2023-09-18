# version: 0.0.1
# author: picklez
# contains all the set up for proceses/threads management and starts the kicker on those threads

import random as rand
import os
import psutil
import threading
from multiprocessing import *
from pm_kicker import *

cpu_process_count = psutil.cpu_count()
process_limit = cpu_process_count - 2
        
class admin_check:
    def has_admin():
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
        hold = admin_check.has_admin()
        return hold[1]
        
class thread_ops:
    def spawn_threads(thread_count,config):
        for x in range(thread_count):
            thread = threading.Thread(target=kicker,args=(x,config,))
            thread.start()
            thread.join()

class process_ops:
    def spawn_process(thread_count, config):
        proc = Process(target=thread_ops.spawn_threads, args=(thread_count,config,))
        proc.start()
        proc.join()
        
    def this_process_esc(config):
        if config['escalate_py'] == True:
            if admin_check.has_admin_simply() == True:
                pid = os.getpid()
                process = next((proc for proc in psutil.process_iter() if proc.pid == pid),None)
                process.nice(psutil.REALTIME_PRIORITY_CLASS)
        
def kicker(threadID, config): # this is where give the script your concurrent task!
    process_ops.this_process_esc(config)
    process = psutil.Process()
    
    task()
    
    return