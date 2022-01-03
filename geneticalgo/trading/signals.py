import ta


def bollinger_bands(df, window=20, deviation=2):
    # Initialize Bollinger Bands Indicator
    indicator_bb = ta.volatility.BollingerBands(close=df["Close"], window=window, window_dev=deviation)

    # Add Bollinger Bands features
    # df['bb_bbm'] = indicator_bb.bollinger_mavg()
    # df['bb_bbh'] = indicator_bb.bollinger_hband()
    # df['bb_bbl'] = indicator_bb.bollinger_lband()

    # Add Bollinger Band high indicator
    # df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

    # Add Bollinger Band low indicator
    df[f'bb_{window}_bbli'] = indicator_bb.bollinger_lband_indicator()
    
    return df


def sma_cross(df_stock, sma1, sma2):
    # GoldenCross 50er>200er
    signal_list=[]
    df_stock[f"sma_{sma1}"]= ta.trend.SMAIndicator(df_stock["Close"], window=sma1, fillna=True).sma_indicator()
    df_stock[f"sma_{sma2}"] = ta.trend.SMAIndicator(df_stock["Close"], window=sma2, fillna=True).sma_indicator()
    for i in df_stock.index:     
        if i-1 in df_stock.index:
            if ((df_stock.iloc[i][f"sma_{sma1}"] > df_stock.iloc[i][f"sma_{sma2}"]) & (df_stock.iloc[i-1][f"sma_{sma1}"] < df_stock.iloc[i-1][f"sma_{sma2}"])):
                signal_list.append(1.0)
                    
            else:
                signal_list.append(0)
        else:
            signal_list.append(0)
    return signal_list


def price_sma_cross(df_stock, sma1):
    # price crosses sma from below
    signal_list=[]
    df_stock[f"sma_{sma1}"]= ta.trend.SMAIndicator(df_stock["Close"], window=sma1, fillna=True).sma_indicator()
    for i in df_stock.index:     
        if i-1 in df_stock.index:
            if ((df_stock.iloc[i][f"sma_{sma1}"] < df_stock.iloc[i]["Close"]) & (df_stock.iloc[i-1][f"sma_{sma1}"] > df_stock.iloc[i-1]["Close"])):
#                     print("buy")
                signal_list.append(1.0)
                    
            else:
#                print("Hold")
                signal_list.append(0)
        else:
            signal_list.append(0)
    return signal_list


def price_ema_cross(df_stock, ema1,ema2):
    # Price > EMA1 && EMA2 (price crosses both emas from below)
    # typical 20erEMA and 50erEMA
    signal_list=[]
    df_stock[f"ema_{ema1}"]= ta.trend.EMAIndicator(df_stock["Close"], window=ema1, fillna=True).ema_indicator()
    df_stock[f"ema_{ema2}"]= ta.trend.EMAIndicator(df_stock["Close"], window=ema2, fillna=True).ema_indicator()
    for i in df_stock.index:     
        if i-1 in df_stock.index:
            if ((df_stock.iloc[i]["Close"] > df_stock.iloc[i][f"ema_{ema1}"]) & (df_stock.iloc[i]["Close"] > df_stock.iloc[i][f"ema_{ema2}"]) & 
                (df_stock.iloc[i-1]["Close"] < df_stock.iloc[i-1][f"ema_{ema1}"]) & (df_stock.iloc[i-1]["Close"] < df_stock.iloc[i-1][f"ema_{ema2}"])):
                signal_list.append(1.0)
                    
            else:
#                print("Hold")
                signal_list.append(0)
        else:
            signal_list.append(0)
    return signal_list


def adx(df_stock, adx, window):
    # Adx is above 25 
    # Window typical 14
    signal_list=[]
    df_stock[f"adx_{adx}"] = ta.trend.ADXIndicator(high=df_stock["High"], low=df_stock["Low"], close=df_stock["Close"], window=window, fillna=True).adx()
    # variante 1 if adx>25 --> 1
    for i in df_stock.index:     
        if i-1 in df_stock.index:
            if (df_stock.iloc[i][f"adx_{adx}"]>adx):
                signal_list.append(1.0)
            else:
                signal_list.append(0)
        else:
            signal_list.append(0)
    # variante 2 if adx>25 && adx[-1]<25 --> 1 else 0
    
    return signal_list


def price_bb_cross(df_stock, window, std):
    # price crosses Upper BB from below (typical 20;2  50;2.1 ;  10;1.9)
    signal_list=[]
    df_stock[f"upper_bb_{window}"]=ta.volatility.BollingerBands(close=df_stock["Close"], window=window, window_dev=std, fillna= True).bollinger_hband()
    
    for i in df_stock.index:
        if i-1 in df_stock.index:
            if ((df_stock.iloc[i]["Close"] > df_stock.iloc[i][f"upper_bb_{window}"]) & 
               (df_stock.iloc[i-1]["Close"]< df_stock.iloc[i-1][f"upper_bb_{window}"])):
                signal_list.append(1.0)
            else:
                signal_list.append(0)
        else:
            signal_list.append(0)
    return signal_list


def macd(df_stock, slow, fast, signal):
    # macd > signal line (typical Macd slow=26, fast=12; signal=9
    # 12ema-26ema; signal=9ema)
    # macd >0
    signal_list=[]
    df_stock[f"macd_s{slow}_f{fast}_si{signal}"]= ta.trend.MACD(close= df_stock["Close"], window_slow=slow, window_fast=fast, window_sign= signal, fillna= True).macd()
    
    for i in df_stock.index:
        if i-1 in df_stock.index:
            if ((df_stock.iloc[i][f"macd_s{slow}_f{fast}_si{signal}"]>0) & 
               (df_stock.iloc[i-1][f"macd_s{slow}_f{fast}_si{signal}"]<0)):
                signal_list.append(1.0)
            else:
                signal_list.append(0)
        else:
            signal_list.append(0)
    return signal_list
