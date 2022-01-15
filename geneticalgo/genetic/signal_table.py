import pandas as pd
from geneticalgo.trading.objective import signal_table


ticker_list = ["AAL", "ALK", "APD", "AEP", "AXP", "AFL", "AIG", "AME", "AMGN", "ADI", "APA", "ADM"]


def get_ticker_list():
    return ticker_list


def split_df(df_stock):

    df_training = df_stock.iloc[ : int(0.75*len(df_stock)), : ]

    df_test = df_stock.iloc[int(0.75*len(df_stock))+1 : , : ]

    return df_training, df_test


def signal_table_for_ticker(ticker_list):

    signal_tables = {}

    df_sp = pd.read_csv("../data/2021-12-06_Top25 SP500 daily.csv")
    df_sp["datadate"] = pd.to_datetime(df_sp["datadate"].astype(str), format='%Y%m%d')
    df_sp = df_sp[["datadate", "conm", "tic", "prcod", "prccd", "prchd", "prcld", "cshtrd"]].rename(columns={"prcod": "Open", "prccd": "Close", "prchd": "High", "prcld": "Low", "cshtrd": "Volume"})

    for ticker in ticker_list:
        df_stock = df_sp[df_sp["tic"]=="AAL"]
        df_stock = df_stock.drop(columns=["conm", "tic"])
        df_stock = df_stock.sort_values(by="datadate")
        df_stock.reset_index(inplace=True, drop=True)

        df_stock, encoding = signal_table(df_stock)

        signal_tables[ticker] = (df_stock, encoding)

        print(f"Signal table for {ticker} was created")

    return signal_tables