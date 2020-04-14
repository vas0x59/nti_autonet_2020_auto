import math
import threading
from functools import wraps
PI = math.pi
E1 = "e1"
E2 = "e2"
TR_LIGHT_CLR = "tfl"
SIGNS_LIST = "signs"



def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap