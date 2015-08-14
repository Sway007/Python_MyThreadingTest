import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

def consumer(cond):
    """wait for the condition and use the resource"""
    t = threading.currentThread()
    logging.debug('Starting consumer thread %s' % t.getName())
    with cond:
        logging.debug('lock acquired by %s' % t.getName())
        time.sleep(1)
        logging.debug('sleep done %s' % t.getName())
        cond.wait()
        logging.debug('lock release by %s' % t.getName())
        logging.debug('Resource is available to consumer')

def producer(cond):
    """set up the resource to be used by the consumer"""
    logging.debug('Starting producer thread')
    with cond:
        logging.debug('Making resource available')
        cond.notifyAll()
        logging.debug('sleep for 1 s')
        time.sleep(1.0)
        logging.debug('resource produce done <----------------')

lock = threading.Lock()
condition = threading.Condition(lock)
# condition = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
c1.setName('C1')
c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
c2.setName('C2')
p = threading.Thread(name='p', target=producer, args=(condition,))

c1.start()
# time.sleep(2)
c2.start()
# time.sleep(2)
p.start()