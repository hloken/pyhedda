import numpy as np

def sannsynlighetsfunksjon(b):
    def p(n):        
        sannsynlighet = 2 * (1 - 1/(1 + np.exp(-b * n)))
        return sannsynlighet
    return p

def flytte_funksjon(x_celler, y_celler):
    def flytt(bakterie):
        dx = np.random.choice([-1, 1])
        dy = np.random.choice([-1, 1])
        
        if bakterie.x + dx >= 0:
            bakterie.x += dx            
        elif bakterie.x + dx < bakterie.x_celler:
            bakterie.x += dx
        
        if (bakterie.y + dy >= 0):
            bakterie.y += dy
        elif (bakterie.y + dy < bakterie.y_celler):
            bakterie.y += dy
        
        return bakterie
    return flytt

class Bakterie(object):
    def __init__(self, x_celler, y_celler, x=None, y=None, resistans=None):
        # Definer startegenskapene til bakterien
        if resistans is None:
            self._resistans = 0
        else:
            self._resistans = resistans

        self._x_celler = x_celler
        self._y_celler = y_celler

        if x is None:
            self._x = np.random.randint(0, x_celler)
        else:
            self._x = x
        
        if y is None:
            self._y = np.random.randint(0, y_celler)
        else:
            self._y = y

        self._alder = 0

    @property
    def x_celler(self):
        return self._x_celler

    @property 
    def y_celler(self):
        return self._y_celler
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, ny_x):
        self._x = ny_x

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, ny_y):
        self._y = ny_y

    @property
    def alder(self):
        return self._alder
    
    @alder.setter
    def alder(self, ny_alder):
        self._alder = ny_alder

    @property
    def posisjon(self):
        return (self.x, self.y)
    
    @posisjon.setter
    def posisjon(self, ny_posisjon):
        self.x = ny_posisjon[0]
        self.y = ny_posisjon[1]
    

    @property
    def resistans(self):
        return self._resistans

    
    @resistans.setter
    def resistans(self, ny_resistans):
        self._resistans = ny_resistans


    def __str__(self):
        return f"""Bakterie(
            x = {self.x}
            y = {self.y}
            posisjon = {self.posisjon}
            alder = {self.alder}
            resistans = {self.resistans}
        )"""



if __name__ == "__main__":
    bakterie = Bakterie(
        x_celler=10,
        y_celler=10,
        x=5,
        y=5,
        antibiotika_resistans=None,
    )

    print(bakterie)
        

        