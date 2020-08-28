import time
import logging


def time_it(original_function):
    """Log time of executed function.

    :param original_function: function which execution time is measured
    :type original_function: function
    :return: wrapper
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        t1 = time.time()
        original_function(*args, **kwargs)
        t2 = time.time()
        logging.info('{} complete in {:.2f} seconds.'.format(original_function.__name__, t2 - t1))

    return wrapper
