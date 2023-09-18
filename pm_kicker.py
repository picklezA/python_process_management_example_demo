# version: 0.0.1
# author: picklez
# runs the given task!

import random as rand

def task():
    output = ""
    for x in range(100):
        output += str(rand.randrange(0,9))
    print(output)