import sys
from time import sleep
from random import uniform
import builtins as __builtin__
            
def print(*args, veloce=False, ritardo=0.01, **kwargs):
    if veloce:
        ritardo=0
        return __builtin__.print(*args, **kwargs)
    sep = kwargs.get('sep','')
    end = kwargs.get('end','\n')
    i=1
    lun = len(args)
    for stringa in args:
        if not(i==1 or i==lun):
            #sleep(uniform(0,0.1))
            sleep(ritardo)
            sys.stdout.write(sep)
            sys.stdout.flush()            
        for char in stringa:
            if char!=' ':
                sleep(ritardo)
            sys.stdout.write(char)
            sys.stdout.flush()
        i += 1
    sleep(ritardo)
    sys.stdout.write(end)
    sys.stdout.flush()    