# importing the required modules
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as xl

sp_url = r'https://docs.google.com/spreadsheets/d/14HeBaRujaYVWf8hsCzFWNC1-NTlhHEHq6aPOsxvAWto/export?format=xlsx'

df = pd.read_excel(sp_url, sheet_name='DB')

st.title('Performance of the 3000 Brands')

#df = pd.read_excel('DB_Performance_SFG.xlsx')
df = df.drop(columns=['GL', 'File_Name', 'Brand_Code'])
Acc_lst = ['TOTAL:SALES', 'DISCOUNT', 'NET SALES', 'COST OF GOODS SOLD', 'GROSS PROFIT', 'TOTAL EXPENSE', 'NET PROFIT BEFORE TAX']
df = df[df['ACC Name'].isin(Acc_lst)]

st.sidebar.header('Please Filter Here')

brand = st.sidebar.multiselect(
    'Select the Brand:',
    options = df['Brand'].unique(),
    #default = df['Brand'].unique()
)

st.sidebar.header('Please Filter Here')

period = st.sidebar.multiselect(
    'Select the Period:',
    options=df['Period'].unique(),
    #default=df['Period'].unique()
)

df_selection = df.query("Brand == @brand & Period == @period")

st.dataframe(df_selection)


#st.write(df)


