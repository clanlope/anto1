from .files_utils import *
from .coms_utils import *
from .webs_utils import *


def timer(func):
    import time, functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"🕒 Execution completed in {end - start:.1f} seconds.")
        return result

    return wrapper
