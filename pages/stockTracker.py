from ast import If
from nsetools import Nse
from pprint import pprint
import pandas as pd
from nsepy import get_history
from datetime import date
import streamlit as st

pd.set_option('display.max_colwidth', None)

IS_DEBUG_ENABLED = False

INDEX_QUOTES_TO_CONSIDER = [
    {"name": "NIFTY 50" },
    {"name": "NIFTY BANK" },
    {"name": "NIFTY MIDCAP 50" },
    {"name": "NIFTY MIDCAP 100" },
    {"name": "NIFTY IT" },
    {"name": "NIFTY SMLCAP 50" }
]

# hQuotes = get_history(symbol='SBIN', start=date(2022,9,1), end=date(2022,9,18)) # Returns DF
# print(hQuotes.head(3))

nseObj = Nse()

# q = nseObj.get_quote('infy')
# df = pd.DataFrame([q])
# print(df)

def getAdvancesAndDeclines():
    adv_dec = nseObj.get_advances_declines()
    df_adv_dec = df = pd.DataFrame(adv_dec)
    printSection("Advances & Declines", df_adv_dec)

def getTopLoosersAndGainers():
    top_losers = nseObj.get_top_losers()
    df_top_loosers = pd.DataFrame(top_losers)
    # df_top_loosers = applyColorToDf("netPrice", df_top_loosers)
    printSection("Top Loosers", df_top_loosers)
    
    top_gainers = nseObj.get_top_gainers()
    df_top_gainers = df = pd.DataFrame(top_gainers)
    printSection("Top Gainers", df_top_gainers)
    return df_top_loosers, df_top_gainers 

def getAllIndexQuotes():
    indexQuotes = []
    for i in INDEX_QUOTES_TO_CONSIDER:
        index_quote = nseObj.get_index_quote(i["name"])
        indexQuotes.append(index_quote)
    index_quotes_df = pd.DataFrame(indexQuotes)
    # print(index_quotes_df)
    # index_quotes_df = index_quotes_df.astype(dtype={'change': 'string', 'pChange': 'string'})
    index_quotes_df['change'] = index_quotes_df['change'].astype(float)
    index_quotes_df['pChange'] = index_quotes_df['pChange'].astype(float)
    index_quotes_df = index_quotes_df.style.applymap(color, subset=['change'])
    printSection("Live Index", index_quotes_df)

def applyColorToDf(column_name, df):
    coloured_df = df.style.applymap(df[column_name])
    return coloured_df

def color(column_name):
    return f"background-color:" + (" #aceeca;" if column_name < 0 else "#FBC3C4") 


def printSection(h3, df):
    if IS_DEBUG_ENABLED:
        print("==============================================================")
        print(h3)
        print(df)
        print("==============================================================") 
    else: 
        st.markdown("### " + h3)
        # dff = df.style.set_properties(**{'background-color': 'black',
        #                    'color': 'green'})
        st.dataframe(df)
    
def app():
    st.markdown("## My Stocks Tracker")
    getAllIndexQuotes()
    getTopLoosersAndGainers()
    getAdvancesAndDeclines()
    
# lot_size = nseObj.get_fno_lot_sizes()
# df_lot_size = pd.DataFrame(lot_size)
# print(df_lot_size)

# index_codes = nseObj.get_index_list()
# index_codes_df = pd.DataFrame(index_codes)
# print(index_codes_df)
