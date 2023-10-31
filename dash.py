import plotly.figure_factory as ff
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import datetime
import openpyxl as xl
import numpy as np
import seaborn as sns

# from datetime import datetime
warnings.filterwarnings('ignore')


def format_number(number):
    return f'{number:,.2f}'


st.title(" :bar_chart: Performance SFG 3000")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

path_db = r"https://github.com/Aussachaa/SFG/raw/main/Database.xlsx"
df = pd.read_excel(path_db, engine="openpyxl", sheet_name='Per19-23')
df['Year'] = df['Year'].astype('str')

# df_chan = df_chan[df_chan['ACC_Name'].isin(['Net Sale', 'Gross Profit'])]

# df_chan_format = df_chan.copy()
# df_chan_format.loc[:, 'JAN': 'Q4'] = df_chan_format.loc[:,'JAN': 'Q4'].applymap(format_number)

# df_chan['AT_FC'] = df_chan['AT_FC'].astype('str')

st.sidebar.header("Choose your filter: ")

# Year
year = st.sidebar.selectbox('Select Year:', df['Year'].unique())
df = df[df['Year'].isin([year])]

# Brand
brand = st.sidebar.multiselect('Pick your Brand:', df['Brand'].unique())
if not brand:
    df2 = df.copy()
else:
    df2 = df[df['Brand'].isin(brand)]

# ACC Name
acc = st.sidebar.selectbox('Select ACC:', df2['ACC Name'].unique())
df2 = df2[df2['ACC Name'].isin([acc])]

# Barh graph
df_tot_ns = df2.sort_values(by=['M01-12'], ascending=False)

st.write(df_tot_ns)

fig = px.bar(df_tot_ns, x='Brand', y='M01-12')
for index, row in df_tot_ns.iterrows():
    fig.add_annotation(
        x=row['Brand'],
        y=row['M01-12'],
        showarrow=False,
        text=str(round(row['M01-12'] / 1000, 1)) + 'M',
        bgcolor="rgba(255, 255, 0, 0.5)")

fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

st.plotly_chart(fig, use_container_width=True)
