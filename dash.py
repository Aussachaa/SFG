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
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

path_file = r'https://github.com/Aussachaa/SFG/raw/main/Peformance_Data.xlsx'
df_chan = pd.read_excel(path_file, engine="openpyxl", sheet_name='Channel')
df_chan = df_chan[df_chan['ACC_Name'].isin(['Net Sale', 'Gross Profit'])]

# df_chan_format = df_chan.copy()
# df_chan_format.loc[:, 'JAN': 'Q4'] = df_chan_format.loc[:,'JAN': 'Q4'].applymap(format_number)

df_chan['AT_FC'] = df_chan['AT_FC'].astype('str')

st.sidebar.header("Choose your filter: ")

# Year
year = st.sidebar.selectbox('Select Year:', df_chan['AT_FC'].unique())
df_chan2 = df_chan[df_chan['AT_FC'].isin([year])]

# Brand
brand = st.sidebar.multiselect('Pick your Brand:', df_chan['Brand'].unique())
if not brand:
    df_chan3 = df_chan2.copy()
else:
    df_chan3 = df_chan2[df_chan2['Brand'].isin(brand)]

# Channel
channel = st.sidebar.multiselect(
    'Pick your Channel:', df_chan2['Channel'].unique())
if not channel:
    df_chan4 = df_chan3.copy()
else:
    df_chan4 = df_chan3[df_chan3['Channel'].isin(channel)]


with st.expander("Data M01-12_ViewData"):
    # st.markdown('### Data M01-12')
    df_chan2_ytd = df_chan4.loc[:, [
        'AT_FC', 'Group_Brand', 'Brand', 'Channel', 'ACC_Name', 'M01-12']]
    df_chan2_ytd_unstk = df_chan2_ytd.set_index(
        ['ACC_Name', 'AT_FC', 'Group_Brand', 'Brand', 'Channel'])
    df_chan2_ytd_unstk = df_chan2_ytd_unstk.unstack(level=0)
    df_chan2_ytd_unstk = df_chan2_ytd_unstk.droplevel([0], axis=1)
    df_chan2_ytd_unstk.columns.name = None
    df_chan2_ytd_unstk = df_chan2_ytd_unstk[['Net Sale', 'Gross Profit']]
    df_chan2_ytd_unstk.reset_index(inplace=True)
    #df_chan2_ytd_unstk.set_index('AT_FC', inplace=True)
    cm = sns.light_palette("green", as_cmap=True)
    st.dataframe(df_chan2_ytd_unstk.style.background_gradient(
        cmap=cm, axis=0), use_container_width=True)
