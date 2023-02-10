import time

class Zone:
    def __init__(self) -> None:
        self.temp = 20
        self.damper = 50
        
    def getTemp(self):
        return self.temp 

    def setDamper(self, percent):
        self.damper= percent
    
    def updateTemp(self, ms):
        initialTime = time.monotonic_ns()
        pastTime = time.monotonic_ns()
        while 1:
            pastTime = time.monotonic_ns()
            if ((pastTime - initialTime) * 1000000) >= ms:
                return self.temp
            pastTime = initialTime
