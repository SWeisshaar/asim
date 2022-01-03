from .signals import *


def signal_table(df_stock):
    
    index = 0
    encoding = {}
    
    # Add the typical price
    df_stock['Typical_Price'] = (df_stock['Close'] + df_stock['Low'] + df_stock['High'])/3
    
    # Adding bollinger bands indicators to table
    for window_size in [7, 20, 30, 60]:
        bollinger_bands(df_stock, window=window_size, deviation=2)
        encoding[index] = f"bb_{window_size}_bbli"
        index += 1

    # Add sma cross
    df_stock["sma_cross"]=sma_cross(df_stock, 50, 200)
    encoding[index] = f"sma_cross"
    index += 1

    # # Add price sma cross
    # df_stock["price_sma_cross"]=price_sma_cross(df_stock, 20)
    # encoding[index] = f"price_sma_cross"
    # index += 1

    # # Add price ema cross
    # df_stock["price_ema_cross"]=price_ema_cross(df_stock,20, 50)
    # encoding[index] = f"price_ema_cross"
    # index += 1

    # # Add price bb cross
    # df_stock["price_bb_cross"]=price_bb_cross(df_stock,20,2)
    # encoding[index] = f"price_bb_cross"
    # index += 1

    # # Add adx
    # df_stock["adx"]=adx(df_stock,25,14)
    # encoding[index] = f"adx"
    # index += 1

    # # Add macd
    # df_stock["macd"]=macd(df_stock,26,12,9)
    # encoding[index] = f"macd"
    # index += 1
    
    return df_stock, encoding


def buy_signal(index, df_signal, indicators):
    
    signal = True
    
    if len(indicators) != 0:
        for ind in indicators:
            if df_signal.iloc[index][ind] != 1.0:
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


def fitness(genome, df_stock, timeframe):
    
    fitness = 0
    
    df_stock, encoding = signal_table(df_stock)

    length_genome = len(genome)
    length_encoding = len(encoding)

    if length_genome != length_encoding:
        raise Exception(f"The length of the genome ({length_genome}) and the encoding ({length_encoding}) has to be equal!")
    
    indicators = resolve_genome(genome, encoding)
    
    list_return = []
    list_signal = []

    position = False

    total_return = 0

    transactions = 0
    
    # TODO incorporate the timeframe
    
    for i in df_stock.index:
        
        if((buy_signal(i, df_stock, indicators)) & (position == False)):
        
            position = True
            
            transactions += 1
            
            price_buy = df_stock.iloc[i]["Typical_Price"]
            
            list_signal.append(price_buy)
            
        elif(position == True):
            
            net_return = df_stock.iloc[i]["Typical_Price"] - price_buy
            
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