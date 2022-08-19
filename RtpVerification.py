import csv

# This is the small quantity of data file
#with open('KonamiSlotsPlayerBalanceTransactions_RTP.csv', newline='') as csvfile:

class DataTracker:
    def __init__(self):
        self.totalBet = 0
        self.totalWon = 0
        self.spinCount = 0

    def AddDataPoint(self, bet, winnings, shouldSpinIncrement):
        self.totalBet += bet
        self.totalWon += winnings
        if shouldSpinIncrement: self.spinCount += 1

    def print(self, gameName):
        avgTotalBet = self.totalBet / self.spinCount
        avgTotalWon = self.totalWon / self.spinCount
        print(gameName + ": " + str(avgTotalWon / avgTotalBet)) # Sum(totalWon) / Sum(totalBet) = average payout percentage
        print(gameName + ": " + str(self.spinCount))
        print('\n')

fileNames = [
    'KonamiSlotsPlayerBalanceTransations_RTP.csv',
    'KonamiSlotsPlayerBalanceTransactions_RTP_331_335.csv'
]

gameToNums = {}

def AggregateAllDate(fileName):
    with open(fileName, newline='\n') as csvfile:

        csvfile.seek(0) # Strip header
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        included_cols = [2, 4, 5]

        for row in reader:

            # Pull out only the columns for amount bet amount won, as well as the name of the game for bucketing
            content = list(row[i] for i in included_cols)
            gameName = content[0]
            
            try:
                amountBet = int(content[1])
            except ValueError:
                amountBet = None

            try:
                amountWon = int(content[2])
            except ValueError:
                amountWon = None

            someDataIsMissing = (amountBet is None or amountWon is None)

            #Remove bad data
            if someDataIsMissing:
                amountBet = 0
                amountWon = 0

            # Sum bets and winnings, track data points as spins (Note: I don't actually know if each data point corresponds to a single spin)
            if gameName not in gameToNums.keys():
                tracker = DataTracker()
                tracker.AddDataPoint(amountBet, amountWon, True)
                gameToNums[gameName] = tracker
            elif amountBet == 0: # If the bet is zero, I am assuming that the row is a special non-paid phase. If this is true, then spinCount should not be incremented
                gameToNums[gameName].AddDataPoint(amountBet, amountWon, False)
            else:
                gameToNums[gameName].AddDataPoint(amountBet, amountWon, True)

for fileName in fileNames:
    AggregateAllDate(fileName)
for game in gameToNums:
    gameToNums[game].print(game)