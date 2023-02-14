import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#US NGB corr plot
US_NGB_df = pd.read_csv('C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\fluxnet_soil_data\\US_NGB.csv'
                             '', skiprows=lambda x: x in list(range(0,5)) + [6])

columns_to_exclude = ['Northing', 'Easting','Diameter_Core_Section', 'Thickness_Core_Section', 'Soil_Wet_Weight',
                      'Wet_Bulk_Density ','Mass_of_Water', 'Mass_of_Organic', 'Mass_of_Mineral']
US_NGB_df_subset = US_NGB_df.drop(columns=columns_to_exclude)

# Min and Max flux for the time of sampling
start = 0.84764
stop = 2.67002

# Define the step size between the values
step = (stop-start)/106

# Create a sequence of float values
values = np.arange(start, stop, step)

# Repeat the values n times to create a column with n rows
US_NGB_df_subset['CH4_Flux'] = values

# create corr matrix
categorical_col = ['Core_Sample_ID', 'Geomorph_Feature', 'Polygon_feature', 'Fe2+_iron ']
US_NGB_df_corr_df = US_NGB_df_subset.drop(columns=categorical_col)

US_NGB_df_corr_df = US_NGB_df_corr_df.apply(pd.to_numeric, errors='coerce')

# compute the correlation coefficients between the constant column and all other columns
corr_matrix = US_NGB_df_corr_df.corr()['CH4_Flux']

sorted_corr = corr_matrix.sort_values(ascending=False)

# plot the correlation matrix as a heatmap
sns.heatmap(corr_matrix.to_frame(), cmap='coolwarm', annot=True, fmt='.2f')
plt.show()

# the whole correlation matrix
cor_mat = US_NGB_df_corr_df.corr()
# plot the correlation matrix as a heatmap
sns.heatmap(cor_mat, cmap='coolwarm', annot=True, fmt='.2f')
plt.show()

# MY_MLM Site corr plot
MY_MLM_df = pd.read_csv('C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\fluxnet_soil_data\\MY_MLM.csv')
categorical_col = ['Sample']
MY_MLM_df_subset = MY_MLM_df.drop(columns=categorical_col)
MY_MLM_df_subset  = MY_MLM_df_subset .apply(pd.to_numeric, errors='coerce')

# Min and Max flux for the time of sampling
start = 18.84121
stop = 39.28005

# Define the step size between the values
step = (stop-start)/3

# Create a sequence of float values
values = np.arange(start, stop, step)

# Repeat the values n times to create a column with n rows
MY_MLM_df_subset['CH4_Flux'] = values

# compute the correlation coefficients between the constant column and all other columns
corr_matrix = MY_MLM_df_subset.corr()['CH4_Flux']

sorted_corr = corr_matrix.sort_values(ascending=False)

# plot the correlation matrix as a heatmap
sns.heatmap(corr_matrix.to_frame(), cmap='coolwarm', annot=True, fmt='.2f')
plt.show()

# the whole correlation matrix
cor_mat = MY_MLM_df_subset.corr()
# plot the correlation matrix as a heatmap
sns.heatmap(cor_mat, cmap='coolwarm', annot=True, fmt='.2f')
plt.show()

# US_DPW corr plot
US_DPW_df = pd.read_csv('C:\\Users\\mcgr323\\projects\\ch4_co2_synthesis\\fluxnet_soil_data\\US_DPW.csv')
US_DPW_df_subset = US_DPW_df[['soilInWaterpH', 'soilInCaClpH']]
US_DPW_df_subset = US_DPW_df_subset .apply(pd.to_numeric, errors='coerce')

# Min and Max flux for the time of sampling
start = 19.38911
stop = 412.77549

# Define the step size between the values
step = (stop-start)/30

# Create a sequence of float values
values = np.arange(start, stop, step)

# Repeat the values n times to create a column with n rows
US_DPW_df_subset['CH4_Flux'] = values

# compute the correlation coefficients between the constant column and all other columns
corr_matrix = US_DPW_df_subset.corr()['CH4_Flux']

sorted_corr = corr_matrix.sort_values(ascending=False)

# plot the correlation matrix as a heatmap
sns.heatmap(corr_matrix.to_frame(), cmap='coolwarm', annot=True, fmt='.2f')
plt.show()

# the whole correlation matrix
cor_mat = US_DPW_df_subset.corr()
# plot the correlation matrix as a heatmap
sns.heatmap(cor_mat, cmap='coolwarm', annot=True, fmt='.2f')
plt.show()

