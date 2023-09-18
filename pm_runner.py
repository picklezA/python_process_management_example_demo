# version: 0.0.6
# author: piclez
# initializes the processes/threads and begins the kicker with cmd line input

from pm_helper import *
import time
start_time = time.time()
import argparse
parser = argparse.ArgumentParser(description="Valid Arguments for Process list getting", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-espy","--escalate_py",action="store_true",help="Will escalate Python processes to realtime (need to be admin to do)")
parser.add_argument("-t","--threads",type=int,help="How many threads you would like to assign to the processes.")
args = parser.parse_args()
config = vars(args)
    
if __name__ == "__main__":
    print("Starting processes & threads!")
    amnt_of_threads = 5 # by default we assign 5 threads
    if config['threads']:
        amnt_of_threads = config['threads']
    for x in range(process_limit):
        process_ops.spawn_process(amnt_of_threads, config)
    print("Welcome back to the main thread! It took "+str(round(time.time()-start_time,2))+"s to run everything!")