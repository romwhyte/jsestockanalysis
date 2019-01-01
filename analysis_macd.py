import pandas as pd
import numpy as np


def getMvgAvg(quotes, points, title):
    #Function takes the average of points number of ticks.
    
    quotes[title] = float('NaN')
    Sum = 0

    for n in range(0,points):
        Sum = Sum + quotes.AdjClose[n]
    MvgAvg = Sum / points
    quotes[title][n] = float('%.4f' % (MvgAvg))

    for n in range(points,len(quotes)):
        Sum = Sum - quotes.AdjClose[n-points] + quotes.AdjClose[n]
        MvgAvg = Sum / points
        quotes[title][n] = float('%.4f' % (MvgAvg))

    return quotes

def getMACDMvgAvg(quotes, points):
    #Function takes the average of points number of ticks.
    title = 'MACDMvgAvg' + str(points)
    quotes[title] = float('NaN')
    Sum = 0

    for n in range(26,26+points):
        Sum = Sum + quotes.MACD[n]
    MvgAvg = Sum / points
    quotes[title][n] = float('%.4f' % (MvgAvg))

    for n in range(26+points,len(quotes)):
        Sum = Sum - quotes.MACD[n-points] + quotes.MACD[n]
        MvgAvg = Sum / points
        quotes[title][n] = float('%.4f' % (MvgAvg))

    return quotes
    
def getMACDSignal(quotes):
    quotes['MACD'] = float('NaN')

    for n in range(26,len(quotes)):
        MACD = quotes.MvgAvgShort[n] - quotes.MvgAvgLong[n]
        quotes['MACD'][n] = float('%.4f' % (MACD))

    return quotes
    
def getMACDTrigger(quotes):
    quotes['MACDTrigger'] = float('NaN')

    for n in range(26,len(quotes)):
        if quotes.MACD[n] > 0:
            quotes.MACDTrigger[n] = 1
        else:
            quotes.MACDTrigger[n] = 0
    
    return quotes
