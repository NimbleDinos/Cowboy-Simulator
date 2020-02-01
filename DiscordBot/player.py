import ability

def playerTest():
    print("playerTest")

class playerClass():
    
    id = 0

    # abilities
    Shooting = ability.abilityClass()
    Hat = ability.abilityClass()
    Riding = ability.abilityClass()
    Catching = ability.abilityClass()
    Mining = ability.abilityClass()

    # inventory
    Health = 100
    gold = 0
    gun = 0
    booze = 0
    hat = 0
    horse = 0
    lasso = 0
    pickaxe = 0
    
    def healthCap():
        if self.Health > 100:
            self.Health = 100