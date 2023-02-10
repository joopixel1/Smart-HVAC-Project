#from simulation import Simulation 

class Zone:
    def __init__(self, simul ) -> None:
        self.temp = 20
        self.damper = 0
        self.simul = simul

    def getTemp(self):
        return self.temp
    
    def setDamper(self, percent):
        self.damper = percent
        
    def updateTemp(self):
        if(self.simul.heating):
            self.temp += 1
        elif(self.simul.cooling):
            self.temp -= 1
            