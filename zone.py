#from simulation import Simulation 

class Zone:
    def __init__(self, simul ) -> None:
        self.temp = 20
<<<<<<< HEAD
        self.damper = 10
=======
        self.damper = 1
        self.delta = 1
>>>>>>> 4aa1a585363510f06df42e9246976d71d1bfc1ba
        self.simul = simul

    def getTemp(self):
        return self.temp
    
    def setDamper(self, percent):
        self.damper = percent
        
    def updateTemp(self):
        if(self.simul.heating):
<<<<<<< HEAD
            self.temp += self.damper*(self.simul.heaterTemp - self.temp)/100
        elif(self.simul.cooling):
            self.temp += self.damper*(self.simul.coolerTemp - self.temp)/100
=======
            self.temp += self.damper*self.delta
        elif(self.simul.cooling):
            self.temp -= self.damper*self.delta
>>>>>>> 4aa1a585363510f06df42e9246976d71d1bfc1ba
            