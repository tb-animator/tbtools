import time
import pymel.core as pm

def timer(func):
    def wrapper(*arg, **kw):
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        return func.__name__, 'evaluation time:: ', (t2 - t1)

    return wrapper

def timerVerbose(func):
    def wrapper(*arg, **kw):
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        return func.__name__, 'evaluation time:: ', (t2 - t1), '\nResult::', res

    return wrapper

class decorator:
    def __init__(self):
        pass

    @staticmethod
    def timer(func):
        '''
        Super awesome and cool for profiling a script - outputs the time taken by the function
        :param func:
        :return:
        '''
        def wrapper(*arg, **kw):
            t1 = time.time()
            res = func(*arg, **kw)
            t2 = time.time()
            print  func.__name__, 'evaluation time:: ', (t2 - t1)
            return func.__name__, 'evaluation time:: ', (t2 - t1)

        return wrapper

    @staticmethod
    def timerVerbose(func):
        def wrapper(*arg, **kw):
            t1 = time.time()
            res = func(*arg, **kw)
            t2 = time.time()
            return func.__name__, 'evaluation time:: ', (t2 - t1), '\nResult::', res

        return wrapper

    @staticmethod
    def undoChunk(func):
        """
        Opens a new undo chunk for the current function. Means all maya commands passed in the function will only be
        part of one ctrl+z
        @param func:
        @return:
        """

        def pre(*args, **kwargs):
            pm.undoInfo(openChunk=True)
            return_func = post(*args, **kwargs)
            return return_func

        def post(*args, **kwargs):
            return_func = func(*args, **kwargs)
            pm.undoInfo(closeChunk=True)
            return return_func

        try:
            return pre

        except Exception as e:
            print e.message
            return None

    @staticmethod
    def undoToggle(func):
        """
        Turns the undo queue off during the function. Then back on afterwards. If the function fails it will restore the queue
        @param func: Function
        @return:
        """

        def pre(*args, **kwargs):
            pm.undoInfo(stateWithoutFlush=False)
            return_func = post(*args, **kwargs)
            return return_func

        def post(*args, **kwargs):
            # We need to be careful with turning off the undo. the finally will always turn it on even with a fail
            try:
                return_func = func(*args, **kwargs)
            except Exception as e:
                return_func = None
                pm.warning(e.message)

            finally:
                pm.undoInfo(stateWithoutFlush=True)

            return return_func

        try:
            return pre

        except Exception as e:
            pm.warning(e.message)
            return None