# importing the required modules
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
c

path = r'https://github.com/Aussachaa/SFG/raw/main/DB_Performance_SFG.xlsx'
df = pd.read_excel(path, engine="openpyxl")

# ----------------------------------------------------

df2 = df.drop(columns=['GL', 'File_Name', 'Brand_Code'])

# Filter ACC Name & Period
Acc_lst = ['NET SALES', 'GROSS PROFIT',
           'TOTAL EXPENSE', 'NET PROFIT BEFORE TAX']
df2 = df2[(df2['ACC Name'].isin(Acc_lst)) & (df2['Period'].str.len() == 3)]

# Rename ACC Name
col_idx = ['Brand', 'Period', 'ACC Name', 'ACT_FC']
df2 = df2.set_index(col_idx)
rename_acc = {'GROSS PROFIT': 'Gross Profit',
              'NET SALES': 'Net Sale',
              'TOTAL EXPENSE': 'Expense',
              'NET PROFIT BEFORE TAX': 'Net Profit'}
df2.rename(index=rename_acc, inplace=True, level=2)

# Unstack AC & FC
df2 = df2.groupby(col_idx).sum()
df2 = df2.unstack(level=3)

# Reset index
df2 = df2.droplevel([0], axis=1)
df2.columns.name = None
df2.reset_index(inplace=True)

# Group brand Active & Non-active
brand_active = ['CL', 'CS', 'EF', 'ER', 'ET', 'PL',
                'PS', 'SS', 'CC', 'GL', 'HC', 'HF', 'TM', 'NT']
df2['Brand'] = df2['Brand'].apply(
    lambda x: x if x in brand_active else "Non-active")
df2 = df2.groupby(['Brand', 'Period', 'ACC Name'], as_index=False).sum()

# Adjust columns
df2['Actual'] = df2.apply(lambda x: x['Actual'] * -
                          1 if x['ACC Name'] == 'Expense' else x['Actual'], axis=1)
df2['Forecast'] = df2.apply(lambda x: x['Forecast'] * -
                            1 if x['ACC Name'] == 'Expense' else x['Forecast'], axis=1)
df2['% of Goal'] = df2.apply(
    lambda x: x['Actual'] / x['Forecast'] if x['Forecast'] != 0 else np.NaN, axis=1)

# Sort Month
month_dict = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
              'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
df2 = df2.sort_values('Period', key=lambda x: x.apply(lambda x: month_dict[x]))

# ----------------------------------------------------
# Streamlit create fileter
st.title('Performance of Brands 3000')
df4 = df2.copy()
st.sidebar.header('Please Filter Here')

brand = st.sidebar.selectbox(
    'Select the Brand:',
    options=df4['Brand'].unique(),
    #default = df['Brand'].unique()
)

# ----------------------------------------------------
# Filter Brand
#brand_fil = 'HF'
#df4 = df4.loc[df4['Brand'] == brand_fil]
df4 = df4.query('Brand == @brand')
df4_ns = df4.loc[df4['ACC Name'] == 'Net Sale']
df4_gp = df4.loc[df4['ACC Name'] == 'Gross Profit']
df4_ex = df4.loc[df4['ACC Name'] == 'Expense']
df4_np = df4.loc[df4['ACC Name'] == 'Net Profit']
df_list = [[df4_ns, df4_gp], [df4_ex, df4_np]]
# df_list[1][0]
print(df_list[1][0]['ACC Name'].iat[0])

# ----------------------------------------------------

# Average Acc Name to show the graph
list_lst_avg = []
list_lst_avg_label = []

for r in [0, 1]:
    for c in [0, 1]:
        df = df_list[r][c]
        lst_avg = [df[df.Actual != 0].Actual.mean(
            axis=0, skipna=False)] * len(df.Period)
        list_lst_avg.append(lst_avg)

        lst_avg_label = [None] * len(df.Period)
        value_avg = df[df.Actual != 0].Actual.mean(axis=0, skipna=False)
        lst_avg_label[0] = '{:.0f}K'.format(value_avg)
        list_lst_avg_label.append(lst_avg_label)

arr_lst_avg = [[list_lst_avg[0], list_lst_avg[1]],
               [list_lst_avg[2], list_lst_avg[3]]]

arr_lst_avg_label = [[list_lst_avg_label[0], list_lst_avg_label[1]],
                     [list_lst_avg_label[2], list_lst_avg_label[3]]]

print(arr_lst_avg[0][0])
print(arr_lst_avg_label[1][1])

# ----------------------------------------------------

# Vistualize
fig, ax = plt.subplots(2, 2, figsize=(15, 6.5))

for r in range(ax.shape[0]):
    for c in range(ax.shape[1]):
        df = df_list[r][c]
        x_p = df['Period']
        y_ac = df['Actual']
        y_fc = df['Forecast']
        y_goal = df['% of Goal']
        first_value_acc = df['ACC Name'].iat[0]

        list_avg_ac = arr_lst_avg[r][c]
        list_avg_ac_label = arr_lst_avg_label[r][c]

        # Bar Forecast
        bar_fc = ax[r, c].bar(x_p, y_fc, color='#CAFF70',
                              width=0.75, label='FC', alpha=0.8)

        # Bar Actual
        distance = 0
        # [ 0  1  2  3  4  5  6  7  8  9 10 11]
        position1 = np.arange(len(x_p))
        # [0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3, 9.3, 10.3, 11.3]
        position2 = [s + distance for s in position1]
        bar_ac = ax[r, c].bar(
            position2, y_ac, color='#FF6A6A', width=0.5, label='AC')

        # Line Avg actual
        line_avg_ac = ax[r, c].plot(
            x_p, list_avg_ac, color='#28B463', linestyle='--', linewidth=2, label='Avg AC')

        # Line % of Goal
        ax2 = ax[r, c].twinx()
        line_goal = ax2.plot(x_p, y_goal, color='#8B8378',
                             marker='s', markersize=6, label='% of Goal')

        # Legend
        lines, labels = ax[0, 0].get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        fig.legend(lines + lines2, labels + labels2, fontsize="9",
                   bbox_to_anchor=(0.5, -0.05), loc='lower center', ncol=4)  # loc='upper right'

        # Series name
        plt.xticks([s + distance / 2 for s in position1], x_p)

        # Data label
        for tx, ty in list(zip(x_p, y_goal)):
            ax2.annotate("{:,.1%}".format(ty),
                         (tx, ty),
                         textcoords='offset points',
                         xytext=(0, 8),
                         ha='center',
                         fontsize=8)

        for tx, ty in list(zip(x_p, y_ac)):
            ax[r, c].annotate("{:,.0f}K".format(ty),
                              (tx, ty),
                              textcoords='offset points',
                              xytext=(0, 2),
                              ha='center',
                              fontsize=8,
                              color='#641E16')

        for tx, ty, tz in list(zip(x_p, list_avg_ac_label, list_avg_ac)):
            ax[r, c].annotate(ty,
                              (tx, tz),
                              textcoords='offset points',
                              xytext=(0, 0),
                              ha='right',
                              fontsize=8,
                              color='#008000')

        # Format axis2-Y
        vals = ax2.get_yticks()
        ax2.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

        # Format axis-Y
        vals0 = ax[r, c].get_yticks()
        ax[r, c].set_yticklabels(['{:,.0f}K'.format(x) for x in vals0])

        # Title
        ax[r, c].set_title(first_value_acc + " " + brand)

        plt.grid(linestyle="--", axis='y')
        plt.tight_layout()

plt.suptitle('Monthly Actual vs Forecast Yr2023_' + brand)
plt.tight_layout()
# plt.show()

st.pyplot(fig)
