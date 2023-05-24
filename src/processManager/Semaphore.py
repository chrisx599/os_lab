import sys
sys.path.append('..')
import queue
from utils.logger import logger
from Process import Process

class Semaphore():
    def __init__(self, initial:int) -> bool:
        """
        initial:the initial value of Semaphore
        return a bool value, False represent failed to init semaphore, True represent successfully
        init semaphore
        """
        if initial <= 0:
            logger.error("the input number of initial value is wrong")
            return False
        logger.info("successfully init semaphore")
        self.value = initial
        self.queue = queue.Queue()
        return True

    def wait(self):
        self.value -= 1
        if self.value < 0:
            # acquire this process
            process = Process.get_running_pcb()
            # add this process to queue
            self.queue.put(process)
            # block()
            pass
    
    def signal(self):
        self.value += 1
        if self.value <= 0:
            process = Process.get_running_pcb()
            # remove a process P from queue
            # wakeup(P)
            pass


test = Semaphore(4)