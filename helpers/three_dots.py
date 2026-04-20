import time

def tdt():
    for _ in range(3):
        print('.', end='', flush=True)
        time.sleep(0.5)
    print('\n')