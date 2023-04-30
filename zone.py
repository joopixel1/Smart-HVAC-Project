#from simulation import Simulation 

class Zone:
    def __init__(self, simul ) -> None:
        self.temp = 22
        self.damper = 10
        self.simul = simul

    def getTemp(self):
        return self.temp
    
    def setDamper(self, percent):
        self.damper = percent
    
    def getDamper(self):
        return self.damper
        
    def updateTemp(self):
        if(self.simul.heat):
            self.temp += ((100 - self.damper)*(self.simul.heaterMaxTemp - self.temp)/100) / 20
        if(self.simul.cool):
            self.temp += ((100 - self.damper)*(self.simul.coolerMaxTemp - self.temp)/100) / 20
            