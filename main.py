# importing the required modules
import streamlit as st
import pandas as pd
import openpyxl as xl

path = r'https://github.com/Aussachaa/SFG/raw/main/DB_Performance_SFG.xlsx'
df = pd.read_excel(path, engine="openpyxl")

st.title('Performance of Brands 3000')

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


