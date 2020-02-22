import math

def calculateLevel(playerXP):
    playerLevel = math.sqrt((playerXP/5)-20)
    return playerLevel