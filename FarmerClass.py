#Represents the player
class Farmer(object):
    def __init__(self,balance,seedLong,seedShort):
        self.seedLong = seedLong
        self.seedShort = seedShort
        self.balance = balance

    def drawFarmerStats(self,canvas,width):
        scoreMarginX = 1.17
        scoreMarginY = 20
        canvas.create_text(width/scoreMarginX, scoreMarginY, 
                text = "Balance: $" +str(self.balance),font = "Aeiral 14 bold")
        longSeed = "Long seeds: " + str(self.seedLong)
        shortSeed = "Short seeds: " + str(self.seedShort)
        canvas.create_text(width/scoreMarginX,2.5*scoreMarginY, text = longSeed,
                                font = "Aerial 14 bold")
        canvas.create_text(width/scoreMarginX,4*scoreMarginY, text = shortSeed, 
                                font = "Aerial 14 bold")
