
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
        goldAmount = 0

        if item == "gun":
            goldAmount = itemPrices[0] * amount
        if item == "booze":
            goldAmount = itemPrices[1] * amount
        if item == "hat":
            goldAmount = itemPrices[2] * amount
        if item == "horse":
            goldAmount = itemPrices[3] * amount
        if item == "lasso":
            goldAmount = itemPrices[4] * amount
        if item == "pickaxe":
            goldAmount = itemPrices[5] * amount
        
        if goldAmount - self.gold < 0:
            return 0 # tell player cannot do this
        else:
            self.gold -= goldAmount
            if item == "gun":
                self.gun += amount
            if item == "booze":
                self.booze += amount
            if item == "hat":
                self.hat += amount
            if item == "horse":
                self.horse += amount
            if item == "lasso":
                self.lasso += amount
            if item == "pickaxe":
                self.pickaxe += amount
            
            return 1 # tell player can do this and that it happened

    # sell item
    def sellItem(item, amount):
        goldAmount = 0

        if item == "gun":
            goldAmount = itemPrices[0] * amount
            if amount > self.gun:
                return 1 # tell player cannot do this
            else:
                self.gun -= amount
                self.gold += goldAmount
                return 0 # tell player it done
        if item == "booze":
            goldAmount = itemPrices[1] * amount
            if amount > self.booze:
                return 1 # tell player cannot do this
            else:
                self.booze -= amount
                self.gold += goldAmount
                return 0 # tell player it done
        if item == "hat":
            goldAmount = itemPrices[2] * amount
            if amount > self.hat:
                return 1 # tell player cannot do this
            else:
                self.hat -= amount
                self.gold += goldAmount
                return 0 # tell player it done
        if item == "horse":
            goldAmount = itemPrices[3] * amount
            if amount > self.horse:
                return 1 # tell player cannot do this
            else:
                self.horse -= amount
                self.gold += goldAmount
                return 0 # tell player it done
        if item == "lasso":
            goldAmount = itemPrices[4] * amount
            if amount > self.lasso:
                return 1 # tell player cannot do this
            else:
                self.lasso -= amount
                self.gold += goldAmount
                return 0 # tell player it done
        if item == "pickaxe":
            goldAmount = itemPrices[5] * amount
            if amount > self.pickaxe:
                return 1 # tell player cannot do this
            else:
                self.pickaxe -= amount
                self.gold += goldAmount
                return 0 # tell player it done

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