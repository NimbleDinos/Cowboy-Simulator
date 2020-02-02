# Discord Imports
import ability
import random

# Other File Imports
import logisticFunc

locationList = ["hull", "lincoln", "sheffield", "corral", "gold-mine", "plains", "river", "shooting-range"]


def playerTest():
    print("playerTest")


class playerClass():
    id = 0
    currentLocation = "town"

    # abilities
    Shooting = ability.AbilityClass()
    Hattitude = ability.AbilityClass()
    Riding = ability.AbilityClass()
    Catching = ability.AbilityClass()
    Mining = ability.AbilityClass()

    # inventory
    health = 100
    gold = 0
    gun = 0
    booze = 0
    hat = 0
    horse = 0
    lasso = 0
    pickaxe = 0
    
    def panAction(self):
        chanceToFindGold = 0.1 # Don't replace this one
        randomNumber = random.uniform(0, 1)
        if chanceToFindGold > randomNumber:
            self.gold += 1
        
        # random generator to pick ability to level up
        randomAbility = random.randint(0, 4)
        if randomAbility == 0:
            self.Shooting.updateXP()
        if randomAbility == 1:
            self.Hattitude.updateXP()
        if randomAbility == 2:
            self.Riding.updateXP()
        if randomAbility == 3:
            self.Catching.updateXP()
        if randomAbility == 4:
            self.Mining.updateXP()
        
        print("chanceToFindGold: " + str(chanceToFindGold))
        print("randomNumber: " + str(randomNumber))
        print("randomAbility: " + str(randomAbility))
        
        print("XP:" +str(self.Shooting.XP))
        print("XP:" +str(self.Hattitude.XP))
        print("XP:" +str(self.Riding.XP))
        print("XP:" +str(self.Catching.XP))
        print("XP:" +str(self.Mining.XP))

    def mineAction(self):
        ChanceToFindGold = logisticFunc.logistic_func(self.Mining.level)
        print(ChanceToFindGold)

    # stops health going above 100
    def healthCap(self):
        if self.health > 100:
            self.health = 100

    # sets new location
    def goToLocation(self, location):
        check = False

        if location in locationList:
            # send message to move to new location here
            check = True

        if check:
            return 0
        else:
            return 1

    # changes players location when game says they have arrived
    def updateLocation(self, location):
        self.currentLocation = location

