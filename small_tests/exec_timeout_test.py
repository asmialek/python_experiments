import multiprocessing
import time


def test_run(queue, arg='Start:'):
    print(arg)
    code = """
i = 0
"""
    try:
        exec(code)
    except Exception as e:
        queue.put(e)
    queue.put(0)


if __name__ == '__main__':
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=test_run, args=(q, 'Hello!'))
    p.start()

    print('>> Interrupt')

    start_time = time.time()

    while p.is_alive():
        if time.time() - start_time > 3:
            print('Killing process!')
            p.terminate()
            p.join()
            break
    else:
        print('> else')
        rtr_value = q.get()
        if isinstance(rtr_value, BaseException):
            raise rtr_value
        elif rtr_value is 0:
            print('>> okok')
        else:
            raise RuntimeError('something happened')

