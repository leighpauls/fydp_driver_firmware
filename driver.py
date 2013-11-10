#!/usr/bin/env python

import serial, threading, time, signal, sys

BAUD_RATE = 9600
SERIAL_READ_TIMEOUT = 1.0

class SerialDriver(threading.Thread):
    def __init__(self, tty):
        threading.Thread.__init__(self)
        self.port = serial.Serial(tty, BAUD_RATE, timeout=SERIAL_READ_TIMEOUT)
        self.done = False
        self.doneSignal = threading.Condition()
        self.start()

    def run(self):
        self.doneSignal.acquire()
        try:
            count = 0
            while not self.done:
                data = self.port.readline()
                if len(data) == 0:
                    done = True
                elif data[0] == 'n':
                    count += 1
                elif data[0] == 'c':
                    print count
                    count = 0

        finally:
            self.port.close()
            self.doneSignal.release()

    def kill(self):
        print "trying to kill..."
        self.done = True
        self.doneSignal.acquire()
        print "done killing"

not_killed = True

def run_driver(tty):

    driver = SerialDriver(tty)
    def signal_handler(signum, frame):
        driver.kill()
        sys.exit()
    signal.signal(signal.SIGINT, signal_handler)

    while not_killed:
        time.sleep(1)

if __name__ == '__main__':
    run_driver('/dev/tty.usbmodemfd121')
