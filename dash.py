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

st.title(" :bar_chart: Performance SFG 3000")
path_file = r'https://github.com/Aussachaa/SFG/raw/main/Peformance_Data.xlsx'
df = pd.read_excel(path_file, engine="openpyxl", sheet_name='Channel')

with st.expander("Channel_ViewData"):
    st.write(df)
