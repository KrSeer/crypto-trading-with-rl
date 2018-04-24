# -*- coding: utf-8 -*-
import pandas as pd
import backtrader as bt
from datetime import datetime


DATA_PATH = "datas/kline_4h.h5"

cerebro = bt.Cerebro()

class SmaCross(bt.SignalStrategy):
        params = (('pfast', 10), ('pslow', 30),)
        def __init__(self):
            sma1, sma2 = bt.ind.SMA(period=self.p.pfast), bt.ind.SMA(period=self.p.pslow)
            self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma1, sma2))

h5_store = pd.io.pytables.HDFStore(DATA_PATH)

kline_4h = h5_store['4h'][datetime(2016,1,1):datetime(2017,6,1)]

cerebro.addstrategy(SmaCross)

data = bt.feeds.PandasData(dataname=kline_4h,
                                 fromdate=datetime(2016, 1, 1),
                                 todate=datetime(2017, 6, 1))

cerebro.adddata(data)
cerebro.broker.set_cash(100000.0)

cerebro.run()

cerebro.plot()

