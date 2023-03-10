#from simulation import Simulation 

class Zone:
    def __init__(self, simul ) -> None:
        self.temp = 30
        self.damper = 10
        self.simul = simul

    def getTemp(self):
        return self.temp
    
    def setDamper(self, percent):
        self.damper = percent
        
    def updateTemp(self):
        if(self.simul.heat):
            self.temp += self.damper*(self.simul.heaterTemp - self.temp)/100
        if(self.simul.cool):
            self.temp += self.damper*(self.simul.coolerTemp - self.temp)/100
            