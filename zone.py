#from simulation import Simulation 

class Zone:
    def __init__(self, simul ) -> None:
        self.temp = 20
        self.damper = 1
        self.delta = 1
        self.simul = simul

    def getTemp(self):
        return self.temp
    
    def setDamper(self, percent):
        self.damper = percent
        
    def updateTemp(self):
        if(self.simul.heating):
            self.temp += self.damper*self.delta
        elif(self.simul.cooling):
            self.temp -= self.damper*self.delta
            