import requests
import pandas as pd
import time
import streamlit as st
import altair as alt

pd.set_option('display.max_colwidth', None)
AVERAGE_FACTOR = 22

MF_SCHEME_CODE = [
    {"schemecode": 122639, "name": "Parag Parekh Flexi Cap Regular"},
    {"schemecode": 125350, "name": "Axis Small Cap Fund - Regular Plan - Growth"},
    {"schemecode": 102875, "name": "Kotak-Small Cap Fund - Growth"},
    {"schemecode": 135799, "name": "TATA Digital India Fund Regular Plan"},
    {"schemecode": 112090, "name": "Kotak Flexicap Fund Regular"},
    {"schemecode": 120841, "name": "quant Mid Cap Fund - Growth Option - Direct"}
]

def getHistoricalMFNavData(schemeCode):
    url = "https://api.mfapi.in/mf/"+str(schemeCode) 
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        data = response.json()
        df = pd.DataFrame(data['data'])
        dfToConsider = df.head(AVERAGE_FACTOR)
        return dfToConsider
    else:
        return None

def printStreamlitTemplate(df):
    st.table(df)

def printConsole(dfToConsider):
    print("Aveerage : " + str(dfToConsider["nav"].mean()))
    print(dfToConsider[dfToConsider['nav'] == dfToConsider['nav'].max()])
    time.sleep(2)
    print(dfToConsider[dfToConsider['nav'] == dfToConsider['nav'].min()])
    time.sleep(2)

def searchMfcode(searchTerm):
    urlForSearch = "https://api.mfapi.in/mf/search?q=" + searchTerm
    response = requests.get(urlForSearch)
    if response.status_code == requests.codes.ok:
        data = response.json()
        df = pd.DataFrame(data)
        print(df.head(AVERAGE_FACTOR))

def getMyPortfolioHistoricalData():
    for x in MF_SCHEME_CODE:
        df = getHistoricalMFNavData(x["schemecode"])
        print("=====================================================================")
        print(x["name"])
        dfToConsider = df.head(AVERAGE_FACTOR)
        dfToConsider['nav'] = dfToConsider['nav'].astype(float)
        print(df.head(AVERAGE_FACTOR))
        print("Count : " + str(dfToConsider.count()))
        print("Aveerage : " + str(dfToConsider["nav"].mean()))
        print(dfToConsider[dfToConsider['nav'] == dfToConsider['nav'].max()])
        print(dfToConsider[dfToConsider['nav'] == dfToConsider['nav'].min()])
        time.sleep(5)
        print("=====================================================================")

def app():
    st.markdown("## My Mutual Fund Tracker")
    for x in MF_SCHEME_CODE:
        dfC = getHistoricalMFNavData(x["schemecode"])
        dfC['nav'] = dfC['nav'].astype(float)
        st.markdown("### " + x["name"] + " [" + str(dfC["nav"].mean())+ "]")
        
        tab1, tab2 = st.tabs(["Data", "Chart"])

        with tab1:
            st.table(dfC)
        with tab2:
            source = pd.DataFrame({
                'date': dfC['date'],
                'nav': dfC['nav']
            })
            c = alt.Chart(source).mark_line().encode(
                x='date',
                y=alt.Y('nav', scale=alt.Scale(type="log"))

            ).interactive()
            st.altair_chart(c, use_container_width=True)

            
       
        
