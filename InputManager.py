import RPi.GPIO as GPIO
import math
import time
from threading import Thread
GPIO.setmode(GPIO.BCM)
class ButtonInputManager(Thread):
    
    N1 = 11
    N2 = 8
    N3 = 9
    N4 = 10
    N5 = 24
    N6 = 23
    N7 = 25
    N8 = 22
    N9 = 27
    N10 = 17
    N11 = 18
    N12 = 15
    N13 = 14
    N14 = 4
    N15 = 7
    N16 = 5
    
    
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
    N = [6]
    
    def __init__(self):
        super().__init__()
        GPIO.setup(BreathInputManager.N[0] ,GPIO.IN)
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
        number = GPIO.input(BreathInputManager.N[0])
        return number
    
    def clear(self):
        self.queue = []

    def toString(self):
        return self.queue

if __name__ == "__main__":
    BIM = ButtonInputManager()
    while True:
        print(BIM.queue)
    
    
