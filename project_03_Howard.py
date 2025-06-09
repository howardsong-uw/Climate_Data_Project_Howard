import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

def data_read(file_path):
    df = pd.read_csv(file_path,
                     parse_dates = ["DATE"],
                     date_format = '%Y-%m',
                     usecols = ["DATE","STATION","PRCP","TAVG"]
                    )
    return df

df=data_read(r"C:\Users\Administrator\Desktop\AAE_718\project_03\4039031.csv")

df = df[df['DATE'].dt.year <= 2024]
df['year'] = df['DATE'].dt.year
df_monthly = df.groupby(['STATION', pd.Grouper(key='DATE', freq='M')])['PRCP'].sum().reset_index()
monthly_avg = df_monthly.groupby('DATE')['PRCP'].mean().sort_index()

result = seasonal_decompose(monthly_avg, model='additive', period=12, extrapolate_trend='freq')

fig = result.plot()
fig.set_size_inches(10, 8)
plt.suptitle('Madison Four Site Representative Monthly Mean Precipitation (PRCP) Time Series Decomposition (2014-2024)',
              fontsize=14)
plt.tight_layout()

valid_stations = ["USC00470273","USC00471416","USW00014837"]
df_filtered = df[df['STATION'].isin(valid_stations)].dropna()
monthly_avg_temp = (
    df_filtered
    .groupby([pd.Grouper(key='DATE', freq='M'), 'STATION'])['TAVG']
    .mean()
    .reset_index()
    .groupby('DATE')['TAVG']
    .mean()
    .sort_index()
)
result = seasonal_decompose(monthly_avg_temp, model='additive', period=12, extrapolate_trend='freq')

# 4. 绘制综合时序分解图
fig = result.plot()
fig.set_size_inches(10, 8)
plt.suptitle('Madison Representative Monthly Mean Temperature (Three Stations) Time Series Decomposition (2014–2024)',
              fontsize=14)
plt.tight_layout()