# importing the required modules
import streamlit as st
import pandas as pd
import openpyxl as xl
import matplotlib.pyplot as plt
import numpy as np
import openpyxl as xl
# -------------------------------------------------------------------------------------

path = r'https://github.com/Aussachaa/SFG/raw/main/DB_Performance_SFG.xlsx'
df = pd.read_excel(path, engine="openpyxl")

df = df.drop(columns=['GL', 'File_Name', 'Brand_Code'])
Acc_lst = ['TOTAL:SALES', 'DISCOUNT', 'NET SALES', 'COST OF GOODS SOLD',
           'GROSS PROFIT', 'TOTAL EXPENSE', 'NET PROFIT BEFORE TAX']
df = df[df['ACC Name'].isin(Acc_lst)]
# -------------------------------------------------------------------------------------

col_index = ['Brand', 'ACC Name', 'Period', 'ACT_FC']
rename_dict = {'COST OF GOODS SOLD': 'Cogs', 'DISCOUNT': 'Discount', 'GROSS PROFIT': 'Gross Profit', 'NET SALES': 'Net Sale', 'TOTAL EXPENSE': 'Expense', 'TOTAL:SALES': 'Sale', 'NET PROFIT BEFORE TAX': 'Net Profit'}
month_dict = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}

df2 = df.groupby(col_index).sum()

df2.rename(index=rename_dict, level=1, inplace=True)

df2 = df2.unstack(level=3)

df2 = df2.droplevel([0], axis=1).reset_index()

df2 = df2.loc[(df2['ACC Name'].isin(['Net Sale', 'Gross Profit', 'Net Profit'])) & (df2['Period'].str.len() == 3)]

df2 = df2.sort_values('Period', key = lambda x : x.apply(lambda x : month_dict[x]))
# -------------------------------------------------------------------------------------

df3 = df2.loc[df2['ACC Name'] == 'Net Sale']
# -------------------------------------------------------------------------------------

st.sidebar.header('Please Filter Here')

brand = st.sidebar.selectbox(
    'Select the Brand:',
    options = df3['Brand'].unique(),
    #default = df['Brand'].unique()
)

df4 = df3.query(
    "Brand == @brand")

df4 = df4.drop(columns=['Brand', 'ACC Name'])
df4 = df4.assign(ACperFC=lambda x: (df4['Actual']/df4['Forecast']))
df5 = df4.set_index('Period')
df5['ACperFC'] = df5['ACperFC'].map('{:.2%}'.format)
st.title('Net Sale Actual VS Forecast Yr 2023')
st.markdown('Brand ' + brand)
st.dataframe(df5, use_container_width=True)


x_p = df4['Period']
y_ac = df4['Actual']
y_fc = df4['Forecast']
y_acperfc = df4['ACperFC']

#define subplots
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x_p, y_ac, color='#FF6A6A', width=0.5, label='Actual')
pos = np.arange(len(x_p))
ax.bar([x + 0.3 for x in pos], y_fc, width=0.5,
       color='#CAFF70', alpha=0.8, label='Forecast')

ax2 = ax.twinx()
ax2.plot(x_p, y_acperfc, color='#8B8378', marker='s', markersize=7, alpha=0.5, label='AC/FC')

plt.xticks([r + 0.3/2 for r in range(len(x_p))], df4["Period"])
plt.title('Net Sale_' + brand)
ax.legend(loc='upper right')

# ask matplotlib for the plotted objects and their labels
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

for tx, ty in list(zip(x_p, y_acperfc)):
    ax2.annotate("{:,.1%}".format(ty), (tx, ty), textcoords='offset points', xytext=(
        0, 8), ha='left', fontsize=10)

vals = ax2.get_yticks()
ax2.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
plt.tight_layout()
st.pyplot(fig)
