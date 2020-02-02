
# Other File Imports
import logisticFunc
import ability
import random

locationList = ["hull", "lincoln", "sheffield", "corral", "gold-mine", "plains", "river", "shooting-range", "travelling"]

# item order gun, booze, hat, horse, lasso, pickaxe
itemPrices = [30, 2, 5, 50, 4, 8]

def playerTest():
    print("playerTest")

class playerClass():
    id = 0
    currentLocation = "town"
    inTown = False

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

    def mineAction(self):
        if self.pickaxe > 0:
            chanceToFindGold = logisticFunc.logistic_func(self.Mining.level)
            randomNumber = random.uniform(0, 1)
            if chanceToFindGold > randomNumber:
                self.gold += 3
            self.pickaxe -= 1
            self.Mining.updateXP()

    def ridingAction(self):
        if self.horse > 0:
            self.horse -= 1;
            self.Riding.updateXP()

    def shootingAction(self):
        if self.gun > 0 and self.health > 1:
            self.gun -= 1
            self.Shooting.updateXP()
            
            chanceToBeShot = logisticFunc.logistic_func(self.Shooting.level)
            randomNumber = random.uniform(0, 1)
            if chanceToBeShot < randomNumber:
                self.health -= 1

    def healAction(self):
        if self.health < 100 and self.booze > 0:
            self.health += 4
            self.booze -= 1
            healthCap()

    def hatAction(self):
        if self.hat > 0:
            self.hat -= 1
            self.Hattitude.updateXP()

    def catchAction(self):
        if self.lasso > 0:
            chanceToFindHorse = logisticFunc.logistic_func(self.Catching.level)
            randomNumber = random.uniform(0, 1)
            if chanceToFindHorse > randomNumber:
                self.horse += 1
            self.lasso -= 1
            self.Catching.updateXP()

    # buy item
    def buyItem(item, amount):
        itemValue = 0

        if item == "gun":
            itemValue = itemPrices[0]
        if item == "booze":
            itemValue = itemPrices[1]
        if item == "hat":
            itemValue = itemPrices[2]
        if item == "horse":
            itemValue = itemPrices[3]
        if item == "lasso":
            itemValue = itemPrices[4]
        if item == "pickaxe":
            itemValue = itemPrices[5]

    # sell item
    def sellItem(item, amount):
        pass

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