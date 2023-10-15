import plotly.figure_factory as ff
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import datetime
import openpyxl as xl
import numpy as np

# from datetime import datetime
warnings.filterwarnings('ignore')


def format_number(number):
    return f'{number:,.2f}'


st.title(" :bar_chart: Performance SFG 3000")
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

path_file = r'https://github.com/Aussachaa/SFG/raw/main/Peformance_Data.xlsx'
df_chan = pd.read_excel(path_file, engine="openpyxl", sheet_name='Channel')

df_chan['YTD'] = df_chan.loc[:, 'JAN': 'DEC'].sum(axis=1)

df_chan_format = df_chan.copy()
df_chan_format.loc[:, 'JAN': 'DEC'] = df_chan_format.loc[:,
                                                         'JAN': 'DEC'].applymap(format_number)

with st.expander("Channel_ViewData"):
    st.write(df_chan_format, use_container_width=True)
