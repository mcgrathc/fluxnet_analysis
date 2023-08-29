import pandas as pd
import matplotlib.pyplot as plt
import os

# Read in the data
df = pd.read_csv("C:\\Users\\mcgr323\\OneDrive - PNNL\\ch4_co2_synthesis\\merged_data.csv")

# Extract relevant columns
df_plot = df[['TIMESTAMP', 'FCH4_F', 'SITE_NAME']]

# Convert timestamp to month
df_plot['MONTH'] = pd.to_datetime(df_plot['TIMESTAMP']).dt.month

# Create directory if it doesn't exist
if not os.path.exists('dist_month'):
    os.makedirs('dist_month')

# Plot and save FCH4 by month for each site
for site in df_plot['SITE_NAME'].unique():
    site_df = df_plot[df_plot['SITE_NAME'] == site]

    mean_fch4 = site_df['FCH4_F'].mean()
    median_fch4 = site_df['FCH4_F'].median()

    plt.figure()
    plt.title(site)
    plt.plot(site_df['MONTH'], site_df['FCH4_F'], marker='o', linestyle='none')
    plt.axhline(mean_fch4, color='red')
    plt.axhline(median_fch4, color='green')
    plt.xlabel('Month')
    plt.ylabel('FCH4_F')

    # Save figure
    plt.savefig(f"dist_month/{site}.png")
