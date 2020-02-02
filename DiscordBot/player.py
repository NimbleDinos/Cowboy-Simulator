# Other File Imports
import logisticFunc
import ability
import random

locationList = ["hull", "lincoln", "sheffield", "corral", "gold-mine", "plains", "river", "shooting-range",
                "travelling"]

# item order gun, booze, hat, horse, lasso, pickaxe
itemPrices = [30, 2, 5, 50, 4, 8]


def playerTest():
    print("playerTest")


class playerClass():
    def __init__(self, database, player_id):
        self.database = database
        self.player_id = player_id

    # abilities
    Shooting = ability.AbilityClass()
    Hattitude = ability.AbilityClass()
    Riding = ability.AbilityClass()
    Catching = ability.AbilityClass()
    Mining = ability.AbilityClass()

    def panAction(self):
        chanceToFindGold = 0.1  # Don't replace this one
        randomNumber = random.uniform(0, 1)
        if chanceToFindGold > randomNumber:
            curr_gold_thing = self.database.select_user_gold(self.player_id)
            (curr_gold,) = curr_gold_thing[0]
            # print(curr_gold)
            self.database.update_player_gold(self.player_id, curr_gold + 1)

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
        (pickaxe_count,) = self.database.select_user_pickaxe(self.player_id)[0]
        print(pickaxe_count)
        if pickaxe_count > 0:
            chanceToFindGold = logisticFunc.logistic_func(self.Mining.level)
            randomNumber = random.uniform(0, 1)
            if chanceToFindGold > randomNumber:
                curr_gold_thing = self.database.select_user_gold(self.player_id)
                (curr_gold,) = curr_gold_thing[0]
                # print(curr_gold)
                self.database.update_player_gold(self.player_id, curr_gold + 1)
            self.database.update_player_pickaxe(self.player_id, pickaxe_count - 1)
            self.Mining.updateXP()

    def ridingAction(self):
        (horse_count,) = self.database.select_user_horse(self.player_id)[0]
        if horse_count > 0:
            self.database.update_player_horse(self.player_id, horse_count - 1)
            self.Riding.updateXP()

    def shootingAction(self):
        (gun_count,) = self.database.select_user_gun(self.player_id)[0]
        (health,) = self.database.select_user_health(self.player_id)[0]
        if gun_count > 0 and health > 1:
            self.database.update_player_gun(self.player_id, gun_count - 1)
            self.Shooting.updateXP()

            chanceToBeShot = logisticFunc.logistic_func(self.Shooting.level)
            randomNumber = random.uniform(0, 1)
            if chanceToBeShot < randomNumber:
                self.database.update_player_health(self.player_id, health - 1)

    def healAction(self):
        (health,) = self.database.select_user_health(self.player_id)[0]
        (booze_count) = self.database.select_user_booze(self.player_id)[0]
        if health < 100 and booze_count > 0:
            new_health = health + 4 if health + 4 < 100 else 100
            self.database.update_player_health(self.player_id, new_health)
            self.database.update_player_booze(self.player_id, booze_count - 1)

    def hatAction(self):
        (hats,) = self.database.select_user_hat(self.player_id)[0]
        if hats > 0:
            self.database.update_player_hat(self.player_id, hats - 1)
            self.Hattitude.updateXP()

    def catchAction(self):
        (lasso_count) = self.database.select_user_lasso(self.player_id)[0]
        if lasso_count > 0:
            chanceToFindHorse = logisticFunc.logistic_func(self.Catching.level)
            randomNumber = random.uniform(0, 1)
            if chanceToFindHorse > randomNumber:
                (horse_count,) = self.database.select_user_horse(self.player_id)[0]
                self.database.update_player_horse(self.player_id, horse_count + 1)
            self.database.update_player_lasso(self.player_id, lasso_count - 1)
            self.Catching.updateXP()

    # buy item
    def buyItem(self, item, amount):
        try:
            int_amount = int(amount)

            total_cost = 0
            (current_gold,) = self.database.select_user_gold(self.player_id)[0]

            if item == "gun":
                total_cost = itemPrices[0] * int_amount
            if item == "booze":
                total_cost = itemPrices[1] * int_amount
            if item == "hat":
                total_cost = itemPrices[2] * int_amount
            if item == "horse":
                total_cost = itemPrices[3] * int_amount
            if item == "lasso":
                total_cost = itemPrices[4] * int_amount
            if item == "pickaxe":
                total_cost = itemPrices[5] * int_amount
            if current_gold - total_cost < 0:
                return 0  # tell player cannot do this
            else:
                self.database.update_player_gold(self.player_id, current_gold - total_cost)
                if item == "gun":
                    (gun_count,) = self.database.select_user_gun(self.player_id)[0]
                    self.database.update_player_gun(self.player_id, gun_count + int_amount)
                if item == "booze":
                    (booze_count,) = self.database.select_user_booze(self.player_id)[0]
                    print("BOOZE {0}".format(booze_count))
                    self.database.update_player_booze(self.player_id, booze_count + int_amount)
                if item == "hat":
                    (hat_count,) = self.database.select_user_hat(self.player_id)[0]
                    self.database.update_player_hat(self.player_id, hat_count + int_amount)
                if item == "horse":
                    (horse_count,) = self.database.select_user_horse(self.player_id)[0]
                    self.database.update_player_horse(self.player_id, horse_count + int_amount)
                if item == "lasso":
                    (lasso_count,) = self.database.select_user_lasso(self.player_id)[0]
                    self.database.update_player_lasso(self.player_id, lasso_count + int_amount)
                if item == "pickaxe":
                    (pickaxe_count,) = self.database.select_user_pickaxe(self.player_id)[0]
                    self.database.update_player_pickaxe(self.player_id, pickaxe_count + int_amount)

                return 1  # tell player can do this and that it happened
        except:
            return 3


    # sell item
    def sellItem(self, item, amount):
        try:
            int_amount = int(amount)
            sell_total = 0
            (current_gold,) = self.database.select_user_gold(self.player_id)[0]

            if item == "gun":
                (gun_count,) = self.database.select_user_gun(self.player_id)[0]
                sell_total = itemPrices[0] * int_amount
                if int_amount > gun_count:
                    return 1    # tell player cannot do this
                else:
                    self.database.update_player_gun(self.player_id, gun_count - int_amount)
                    self.database.update_player_gold(self.player_id, sell_total + current_gold)
                    return 0    # tell player it done
            if item == "booze":
                (booze_count,) = self.database.select_user_booze(self.player_id)[0]
                sell_total = itemPrices[1] * int_amount
                if int_amount > booze_count:
                    return 1    # tell player cannot do this
                else:
                    self.database.update_player_booze(self.player_id, booze_count - int_amount)
                    self.database.update_player_gold(self.player_id, sell_total + current_gold)
                    return 0    # tell player it done
            if item == "hat":
                (hat_count,) = self.database.select_user_hat(self.player_id)[0]
                sell_total = itemPrices[2] * int_amount
                if int_amount > hat_count:
                    return 1    # tell player cannot do this
                else:
                    self.database.update_player_hat(self.player_id, hat_count - int_amount)
                    self.database.update_player_gold(self.player_id, sell_total + current_gold)
                    return 0    # tell player it done
            if item == "horse":
                (horse_count,) = self.database.select_user_horse(self.player_id)[0]
                sell_total = itemPrices[3] * int_amount
                if int_amount > horse_count:
                    return 1    # tell player cannot do this
                else:
                    self.database.update_player_horse(self.player_id, horse_count - int_amount)
                    self.database.update_player_gold(self.player_id, sell_total + current_gold)
                    return 0    # tell player it done
            if item == "lasso":
                (lass_count,) = self.database.select_user_lasso(self.player_id)[0]
                sell_total = itemPrices[4] * int_amount
                if int_amount > lass_count:
                    return 1    # tell player cannot do this
                else:
                    self.database.update_player_lasso(self.player_id, lass_count - int_amount)
                    self.database.update_player_gold(self.player_id, sell_total + current_gold)
                    return 0    # tell player it done
            if item == "pickaxe":
                (pickaxe_count,) = self.database.select_user_pickaxe(self.player_id)[0]
                sell_total = itemPrices[5] * int_amount
                if int_amount > pickaxe_count:
                    return 1    # tell player cannot do this
                else:
                    self.database.update_player_pickaxe(self.player_id, pickaxe_count - int_amount)
                    self.database.update_player_gold(self.player_id, sell_total + current_gold)
                    return 0    # tell player it done
        except:
            return 3