import ability

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
