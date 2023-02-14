import pandas as pd
import os
import plotly.express as px


flux_daily_dir = 'C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\fluxnet_flux_data\\flux_daily\\'
soil_dir = 'C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\fluxnet_soil_data\\'


def read_directory_to_dataframe(directory_path):
    file_list = os.listdir(directory_path)
    data_frames = []
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)
        df['file_name'] = file_name
        data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)


def keep_text_in_column(df, column, start, end):
    df[column] = df[column].apply(
        lambda x: x[x.find(start) + len(start):x.find(end)] if x.find(start) != -1 and x.find(end) != -1 else '')
    return df


def get_date_range_by_id(df, id_column, date_column):
    result = {}
    for id_value in df[id_column].unique():
        sub_df = df[df[id_column] == id_value]
        sub_df[date_column] = pd.to_datetime(sub_df[date_column], format='%Y%m%d')
        start_date = sub_df[date_column].min().strftime('%Y%m%d')
        end_date = sub_df[date_column].max().strftime('%Y%m%d')
        result[id_value] = (start_date, end_date)
    return result


def mean_monthly_flux(df, date_column, value_column, identifier_column):
    df[date_column] = pd.to_datetime(df[date_column], format='%Y%m%d')
    df['month'] = df[date_column].dt.month
    df['year'] = df[date_column].dt.year
    mean_values = df.groupby([identifier_column, 'year', 'month'])[value_column].mean()
    mean_values = mean_values.reset_index()
    return mean_values


def plot_monthly_mean_flux(df, identifier_column, value_column, year):
    fig = px.line(df[df['year'] == year], x='month', y=value_column, color=identifier_column, line_group=identifier_column,
                  labels={'month': 'Month', value_column: 'CH4 Flux'})
    fig.update_layout(title=f'Monthly Mean CH4 Flux by Site for {year}',
                      xaxis_title='Month',
                      yaxis_title='CH4 Flux',
                      xaxis=dict(tickmode='linear',
                                 tick0=1,
                                 dtick=1,
                                 tickformat='%B'),
                      margin=dict(l=60, r=20, t=60, b=20),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    fig.show()



df = read_directory_to_dataframe(flux_daily_dir)
keep_text_in_column(df, 'file_name', 'FLX_', '_FLUXNET')
df.rename(columns={'file_name': 'Site'}, inplace=True)

date_range = get_date_range_by_id(df, 'Site', 'TIMESTAMP')
df_dates = pd.DataFrame.from_dict(date_range, orient='index', columns=['start_date', 'end_date'])

columns_to_keep = ['Site', 'TIMESTAMP', 'FCH4', 'WTD', 'NEE']
ch4_df = df[columns_to_keep]

ch4_df = ch4_df[ch4_df['FCH4'] != -9999.00000]

mean_values = mean_monthly_flux(ch4_df, 'TIMESTAMP', 'FCH4', 'Site')
plot_monthly_mean_flux(mean_values, 'Site', 'FCH4', 2018)

# Convert the date column to a datetime object
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%Y%m%d')

# Extract the year from the date column
df['year'] = df['TIMESTAMP'].dt.year

# Group the data by year and unique identifier (id) and calculate the mean of the data column
mean_yearly_flux = df.groupby(['year', 'Site'])['FCH4'].mean().reset_index()






