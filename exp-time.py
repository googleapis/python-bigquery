import time
from functools import wraps

def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} ran in {round(end - start, 2)} seconds")
        #logger.debug("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper

@timed
def slow_function():
    """This is a slow-running function used as an example."""
    print("running a slow function...")
    time.sleep(3.2)
    print("done")

slow_function()