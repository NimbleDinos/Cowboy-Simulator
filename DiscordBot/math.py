import math

def calculateLevel(playerXP):
    if playerXP < 105:
        playerLevel = 0
    else:
        playerLevel = math.sqrt((playerXP/5)-20)
    return playerLevel