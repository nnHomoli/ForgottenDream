import threading
import queue


def timeout(seconds, error_message='Timeout'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result_queue = queue.Queue()
            thread = threading.Thread(target=_timeout_wrapper, args=(func, args, kwargs, result_queue))
            thread.daemon = True
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                raise TimeoutError(error_message)
            return result_queue.get()

        return wrapper

    def _timeout_wrapper(func, args, kwargs, result_queue):
        try:
            result = func(*args, **kwargs)
            result_queue.put(result)
        except Exception as e:
            result_queue.put(e)

    return decorator
