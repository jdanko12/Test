import yfinance as yf
import pandas as pd

ticker_data = []
ticker_data.append(yf.Ticker("QQQ"))
ticker_data.append(yf.Ticker("AAPL"))
ticker_data.append(yf.Ticker("AMZN"))
ticker_data.append(yf.Ticker("MSFT"))
#ticker_data.append(yf.Ticker("GOOGL"))
#ticker_data.append(yf.Ticker("V"))
#ticker_data.append(yf.Ticker("MA"))
#ticker_data.append(yf.Ticker("BAM"))
#ticker_data.append(yf.Ticker("AMD"))
#ticker_data.append(yf.Ticker("NVDA"))
#ticker_data.append(yf.Ticker("PANW"))
#ticker_data.append(yf.Ticker("FTNT"))
#ticker_data.append(yf.Ticker("DDOG"))
#ticker_data.append(yf.Ticker("ENPH"))
#ticker_data.append(yf.Ticker("LULU"))
#ticker_data.append(yf.Ticker("MPWR"))
#ticker_data.append(yf.Ticker("MDB"))
#ticker_data.append(yf.Ticker("PYPL"))
#ticker_data.append(yf.Ticker("SQ"))
#ticker_data.append(yf.Ticker("ZS"))
#ticker_data.append(yf.Ticker("WIRE"))


for ticker in ticker_data:
    # get historical market data
    data = ticker.history(period="max")
    #print(data.index[1])
    data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
    data['EMA10'] = data['Close'].ewm(span=10, adjust=False).mean()
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['EMA100'] = data['Close'].ewm(span=100, adjust=False).mean()

    accountValue = 100000.0
    position = False
    risk = 2.0
    positionSize = 0.0
    stopPercent = 0.04
    entryPrice = 0.0
    stopPrice = 0.0
    exitPrice = 0.0
    tradeBlock = 15
    wins = 0
    losses = 0
    i = 0
    R = 0.0
    size = len(data-1)
    startDate = data.index[0]
    endDate = data.index[size-1]
    

    print(str(risk) + "% Risk Per Trade : " + str(stopPercent*100) + "% SL : " + str(tradeBlock) + " day block after Loss")
    for index, row in data.iterrows():
        #print(str(i) + " EMA10: " + str(row['EMA10']) + " EMA100: " + str(row['EMA100']))
        close_price = row['Close']
        i += 1
        tradeBlock += 1

        if not position and row['EMA5']<row['EMA20'] and tradeBlock>=15:
            position = True
            entryPrice = close_price
            stopPrice = entryPrice + (entryPrice * stopPercent)
            positionSize = ((accountValue*risk) / 100) / (entryPrice-stopPrice) * -1
            print(str(index) + " Entered position: " + str(positionSize) + " shares @ " + str(entryPrice) + ", stop loss: " + str(stopPrice))

        if position and row['Close'] > stopPrice:
            position = False
            exitPrice = row['Close']
            losses += 1
            R = R - 1.0
            accountValue = accountValue - ((exitPrice - entryPrice) * positionSize)
            tradeBlock = 0
            print(str(index) + " L. Stop loss hit, closing position @ " + str(exitPrice) + " R=-1, Account Value: " + str(accountValue))
            print()

        #if position and row['EMA20']>row['EMA100'] and row['Close'] < entryPrice:
        if position and row['Close'] <= entryPrice-(entryPrice*3*stopPercent) and row['Close'] < entryPrice:    
            position = False
            exitPrice = row['Close']
            wins += 1
            r = entryPrice - exitPrice 
            r = (r / entryPrice) * 100
            r = r / (stopPercent*100)
            R = R + r
            accountValue = accountValue + ((entryPrice - exitPrice) * positionSize)
            tradeBlock = 0
            print(str(index) + " W. Closing postition @ " + str(exitPrice) + " R=" +str(r) + " , Account Value: " + str(accountValue))
            print()

    print(ticker)
    print(startDate)
    print(endDate)
    print("Wins: " + str(wins))
    print("Losses: " + str(losses))
    print("Win Rate: " + str(round(wins/(wins+losses), 2)))
    print("Total R: " + str(round(R, 2)))
    print("Account Value: " + str(round(accountValue, 2)) + " : " + str(round((accountValue/100000), 2)) + "X")
    print()
    print()