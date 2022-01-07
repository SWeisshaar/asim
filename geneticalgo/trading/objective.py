from .signals import *


def signal_table(df_stock):
    
    index = 0
    encoding = {}
    
    # Add the typical price
    df_stock['Typical_Price'] = (df_stock['Close'] + df_stock['Low'] + df_stock['High'])/3
    
    # Adding bollinger bands indicators to table
    for window_size in [5, 10, 20, 30, 90]:
        bollinger_bands(df_stock, window=window_size, deviation=2)
        encoding[index] = f"bb_{window_size}_bbli"
        index += 1

    # Add price hbb cross
    for touple in [(20,2), (50,2.1), (10,1.9)]:
        df_stock[f"price_hbb_cross_{touple[0]}_{touple[1]}"]=price_hbb_cross(df_stock,touple[0],touple[1])
        encoding[index] = f"price_hbb_cross_{touple[0]}_{touple[1]}"
        index += 1

    # Add price lbb cross
    for touple in [(20,2), (50,2.1), (10,1.9)]:
        df_stock[f"price_lbb_cross_{touple[0]}_{touple[1]}"]=price_lbb_cross(df_stock,touple[0],touple[1])
        encoding[index] = f"price_lbb_cross_{touple[0]}_{touple[1]}"
        index += 1

    # Add sma cross
    df_stock["sma_cross"]=sma_cross(df_stock, 50, 200)
    encoding[index] = f"sma_cross"
    index += 1

    # Add price sma cross
    for window_size in [14, 20, 40, 60, 100]:
        df_stock[f"price_sma_{window_size}_cross"]=price_sma_cross(df_stock, window_size)
        encoding[index] = f"price_sma_{window_size}_cross"
        index += 1

    # Add ema cross
    df_stock["price_ema_20_50_cross"]=price_ema_cross(df_stock,20, 50)
    encoding[index] = f"price_ema_20_50_cross"
    index += 1

    # Add price ema cross
    df_stock["price_ema_20_cross"]=price_ema_cross(df_stock,20, 20)
    encoding[index] = f"price_ema_20_cross"
    index += 1

    df_stock["price_ema_50_cross"]=price_ema_cross(df_stock,50, 50)
    encoding[index] = f"price_ema_50_cross"
    index += 1

    # Add adx
    df_stock["adx"]=adx(df_stock, 25, 14)
    encoding[index] = f"adx"
    index += 1

    # Add macd
    df_stock["macd"]=macd(df_stock, 26, 12, 9)
    encoding[index] = f"macd"
    index += 1

    print(f"The number of indicators in the genome is {index}")
    
    return df_stock, encoding


def buy_signal(index, df_signal, indicators):
    
    signal = True
    counter = 0
    number_of_indicators = len(indicators)
    percentage = 0.5
    
    if number_of_indicators != 0:
        for ind in indicators:
            if df_signal.iloc[index][ind] != 1.0:
                counter += 1

                if counter > ((1 - percentage) * number_of_indicators):
                    signal = False
                    
                    break
    else:
        signal = False
            
    return signal
    

def resolve_genome(genome, encoding):
    
    list = []
    index = 0
    
    for gen in genome:
        if gen == 1:
            list.append(encoding[index])
        
        index += 1
    
    return list


def fitness(genome, df_signal, encoding):
    
    indicators = resolve_genome(genome, encoding)
    
    list_return = []
    list_signal = []

    position = False

    total_return = 0

    transactions = 0
    
    # TODO incorporate the timeframe
    
    for i in df_signal.index:
        
        if((buy_signal(i, df_signal, indicators)) & (position == False)):
        
            position = True
            
            transactions += 1
            
            price_buy = df_signal.iloc[i]["Typical_Price"]
            
            list_signal.append(price_buy)
            
        elif(position == True):
            
            net_return = df_signal.iloc[i]["Typical_Price"] - price_buy
            
            percentage = 0.05
            
            # Close position if it makes 10 % loss or profit
            if((net_return < -(percentage * price_buy)) |
               (net_return > (percentage * price_buy))):
                
                position = False
                
                transactions += 1
                
                total_return += net_return
                
            list_signal.append(None)
            
        else:
            list_signal.append(None)
                
        list_return.append(total_return)

    print(f"Genome: {genome} with total return: {total_return}")
    
    return total_return, list_return, list_signal