import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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


def plot_month_seasonality(df):
    sites = df['Site'].unique()

    # Define the colors for each year
    colors = {}
    for i, year in enumerate(df['TIMESTAMP'].dt.year.unique()):
        colors[year] = palette[i % len(palette)]

    # Create a plot for each site
    for site in sites:
        subset = df[df['Site'] == site]

        # Group the data by year and month
        grouped = subset.groupby(pd.Grouper(key='TIMESTAMP', freq='M')).mean()

        # Create a plot for the current site
        fig, ax = plt.subplots(figsize=(14, 10))
        for year in grouped.index.year.unique():
            group = grouped[grouped.index.year == year]
            ax.plot(group.index.month, group['FCH4'], color=colors[year], linewidth=3, label=str(year))

        # Set the x-axis to show the months and format the tick labels
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Set the axis labels, title, and legend
        ax.set_xlabel('Month', fontsize=32)
        ax.set_ylabel('Flux (nmol CH$_4$ m$^{-2}$ s$^{-1}$)', fontsize=32)
        ax.set_title(f'Monthly Mean CH$_4$ Flux for {site}', fontsize=32)
        ax.legend(loc="best", fontsize=24)

        # Save the plot to a file
        plt.savefig(f"C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\seasonality\\{site}.png")


def plot_seasonality(df, save_path=None):
    sites = df['Site'].unique()
    for site in sites:
        subset = df[df['Site'] == site]
        subset.replace(-9999.00000, np.nan, inplace=True)

        # Visual inspection
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(subset.index, subset['FCH4'])
        ax.set_xlabel('Date (Month-Year)', fontsize=32)
        ax.set_ylabel('Flux (nmol CH$_4$ m$^{-2}$ s$^{-1}$)', fontsize=32)
        ax.set_title(f'Seasonality Inspection for {site}', fontsize=32)

        # set the x-axis ticks to show only the month and year
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

        # rotate the x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        if save_path:
            plt.savefig(f'{save_path}/{site}_all_data.png')
        else:
            plt.show()


# Run for the fluxnet data
flux_daily_dir = 'C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\fluxnet_flux_data\\flux_daily\\'
df = read_directory_to_dataframe(flux_daily_dir)
keep_text_in_column(df, 'file_name', 'FLX_', '_FLUXNET')
df.rename(columns={'file_name': 'Site'}, inplace=True)


# Convert the date column to a datetime object
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%Y%m%d')
df.replace(-9999.00000, np.nan, inplace=True)

# Create the seasonality plots
plot_month_seasonality(df)

save_path = 'C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\seasonality'

# Loop over the site names and save the plots
for site_name in df['Site'].unique():
    plot_seasonality(df, save_path=save_path)



