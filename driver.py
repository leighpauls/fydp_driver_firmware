#!/usr/bin/env python

import serial, threading
import time, signal, sys
import socket

BAUD_RATE = 9600
SERIAL_READ_TIMEOUT = 1.0
SPEED_DIFF_PERIOD = 0.2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def sendSpeedUpdate(speedString):
    sock.sendto(speedString + "\n", ("0.0.0.0", 4321))

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
            stepQueue = []
            while not self.done:
                data = self.port.readline()
                curTime = time.time()
                if len(data) == 0:
                    continue
                if data[0] == 'c':
                    stepQueue.append(curTime)
                elif data[0] == 'n':
                    None
                while (len(stepQueue) > 0 and 
                       stepQueue[0] < curTime - SPEED_DIFF_PERIOD):
                    stepQueue = stepQueue[1:]
                speed = float(len(stepQueue)) / SPEED_DIFF_PERIOD
                sendSpeedUpdate(str(speed))
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
