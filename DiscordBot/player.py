import ability

locationList = ["hull", "lincoln", "sheffield", "corral", "gold-mine", "plains", "river", "shooting-range"]

def playerTest():
    print("playerTest")

class playerClass():
    
    id = 0
    currentLocation = "town"

    # abilities
    Shooting = ability.abilityClass()
    Hattitude = ability.abilityClass()
    Riding = ability.abilityClass()
    Catching = ability.abilityClass()
    Mining = ability.abilityClass()

    # inventory
    health = 100
    gold = 0
    gun = 0
    booze = 0
    hat = 0
    horse = 0
    lasso = 0
    pickaxe = 0
    
    def healthCap():
        if self.health > 100:
            self.health = 100

    def goToLocation(self,location):
        check = False
        for x in locationList:
            if x == location:
                # send message to move to new location here
                check = True
        
        if check == True:
            return 0
        else:
            return 1