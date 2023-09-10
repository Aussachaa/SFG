# importing the required modules
import streamlit as st
import pandas as pd
import numpy as np
import streamlit_pandas as sp

sp_url = r'https://docs.google.com/spreadsheets/d/14HeBaRujaYVWf8hsCzFWNC1-NTlhHEHq6aPOsxvAWto/export?format=xlsx'
df = pd.read_excel(sp_url, sheet_name='DB')

st.title('Performance of the 3000 Brands')

#df = pd.read_excel('DB_Performance_SFG.xlsx')
df = df.drop(columns=['GL', 'File_Name', 'Brand_Code'])
Acc_lst = ['TOTAL:SALES', 'DISCOUNT', 'NET SALES', 'COST OF GOODS SOLD', 'GROSS PROFIT', 'TOTAL EXPENSE', 'NET PROFIT BEFORE TAX']
df = df[df['ACC Name'].isin(Acc_lst)]

create_data = {
                'Brand': 'multiselect',
                'ACC Name': 'multiselect',
                'Period': 'multiselect'
                }

all_widgets = sp.create_widgets(df, create_data, ignore_columns=['Amount'])
res = sp.filter_df(df, all_widgets)
st.write(res)


