import RPi.GPIO as GPIO
import math
import time
from threading import Thread
GPIO.setmode(GPIO.BCM)
class ButtonInputManager(Thread):
    
    N1 = 7
    N2 = 5
    N3 = 4
    N4 = 14
    N5 = 15
    N6 = 18
    N7 = 17
    N8 = 27
    N9 = 22
    N10 = 23
    N11 = 24
    N12 = 10
    N13 = 9
    N14 = 11
    N15 = 25
    N16 = 8
    N = [N1, N2, N3, N4, N5, N6, N7, N8, N9, N10, N11, N12, N13, N14, N15, N16]
    
    def __init__(self):
        super().__init__()
        for n in ButtonInputManager.N:
            GPIO.setup(n ,GPIO.IN)
        self.queue = []
        self.start()
        
    def run(self):
        while True:
            state = self.getButtonStates()
            if state != 0:
                n = int(math.log(state, 2)) + 1
                self.add(n)
                time.sleep(0.4)

    def pop(self):
        return self.queue.pop(0)

    def add(self, number):
        self.queue.append(number)

    def getButtonStates(self):
        #stri = ""
        number = 0
        for n in range(len(ButtonInputManager.N)):
            #stri += str(GPIO.input(ButtonInputManager.N[n]))
            number += (GPIO.input(ButtonInputManager.N[n]) * (2**n))
        #print(stri)
        return number
    
    def clear(self):
        self.queue = []

    def toString(self):
        return self.queue

class BreathInputManager(Thread):
    N = [21]
    
    def __init__(self):
        super().__init__()
        GPIO.setup(21 ,GPIO.IN)
        self.queue = []
        self.start()
        
    def run(self):
        while True:
            state = self.getButtonStates()
            if state != 0:
                n = int(math.log(state, 2)) + 1
                self.add(n)
                time.sleep(0.4)

    def pop(self):
        return self.queue.pop(0)

    def add(self, number):
        self.queue.append(number)

    def getButtonStates(self):
        number = GPIO.input(21)
        return number
    
    def clear(self):
        self.queue = []

    def toString(self):
        return self.queue

if __name__ == "__main__":
    BIM = ButtonInputManager()
    while True:
        print(BIM.queue)
    
    
