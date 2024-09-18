import pandas as pd
import matplotlib.pyplot as plt
import os

# Print the current working directory
print(os.getcwd())

# Get the path
current_path=os.getcwd()
print(current_path)

# Load the data 
#url = '/Users/macbookpro/Desktop/DSDM/Brush ups/brushup_files/WB data/P_Data_Extract_From_World_Development_Indicators (1)/WB_data_use.csv'
url=current_path+'/WB_data_use.csv'
print(url)
data = pd.read_csv(url)

# show the dimensions
print(data.shape)

# Display the first few rows of the dataset
print(data.head())

# Check for missing values
print(data.isnull().sum())

# Inspect columns
print(data.columns)

# Inspect the data types and basic statistics
print(data.info())
print(data.describe())

# Transform into DataFrame
data_df = pd.DataFrame(data)

# Check unique countries in the dataset
print("Unique countries:", data_df['Country Name'].nunique())
print("Unique countries list:", data_df['Country Name'].unique())

# Reshape the data to have 'Country Name', 'Year', and 'Population' columns
# Unpivoting using pandas' melt function
year_columns = [col for col in data.columns if '[YR' in col]
print(year_columns)

# Unpivot the dataframe
reshaped_data = pd.melt(data, id_vars=['Country Name', 'Country Code'], value_vars=year_columns, var_name='Year', value_name='Population')

# Clean up the 'Year' column to remove the extra text
reshaped_data['Year'] = reshaped_data['Year'].str.extract('(\d{4})').astype(int)
print(reshaped_data['Year'].unique())

# Convert population to numeric
reshaped_data['Population'] = pd.to_numeric(reshaped_data['Population'], errors='coerce')

# Display the reshaped data
print(reshaped_data.head())

# Check for missing values
missing_values = reshaped_data.isnull().sum()

# Get basic statistics of the reshaped data 'Population' column
population_stats = reshaped_data['Population'].describe()
print(missing_values, population_stats)

# Some visuals

# Remove rows with missing population values
cleaned_data = reshaped_data.dropna(subset=['Population'])

# Population Trend Analysis for India (just example of one country)
india_data = cleaned_data[cleaned_data['Country Name'] == 'India']
print(india_data.head())

# matplotlib inline
plt.figure(figsize=(10, 6))
plt.plot(india_data['Year'], india_data['Population'], marker='o', color='blue')
plt.title('Population Trend in India (1990-2023)')
plt.xlabel('Year')
plt.ylabel('Population')
plt.grid(True)
plt.show()


# Thinking about new trend/variable
# Sort data by 'Country Name' and 'Year'
reshaped_data.sort_values(by=['Country Name', 'Year'], inplace=True)

# Calculate the population growth rate for each country (percentage change between consecutive years)
reshaped_data['Population Growth Rate (%)'] = reshaped_data.groupby('Country Name')['Population'].pct_change(fill_method=None) * 100


# Calculate the doubling time using the rule of 70
reshaped_data['Doubling Time (years)'] = 70 / reshaped_data['Population Growth Rate (%)']

# Preview the results
print(reshaped_data[['Country Name', 'Year', 'Population', 'Population Growth Rate (%)', 'Doubling Time (years)']].head(10))

# Calculate the average doubling time for each country
average_doubling_time = reshaped_data.groupby('Country Name')['Doubling Time (years)'].mean().reset_index()

# Handle cases where there are infinite or NaN values in the doubling time (e.g., no growth or negative growth)
average_doubling_time = average_doubling_time.replace([float('inf'), -float('inf')], None).dropna()

# I'm going to cluster them based on the average doubling time.
# I'm making assumptions here and creating 3 categories based on the doubling time: fast (<20 years), medium (20-50 years), slow (>50 years)

def categorize_doubling_time(years):
    if years < 20:
        return 'Fast Doubling'
    elif 20 <= years <= 50:
        return 'Medium Doubling'
    else:
        return 'Slow Doubling'

# Apply the categorization
average_doubling_time['Doubling Time Category'] = average_doubling_time['Doubling Time (years)'].apply(categorize_doubling_time)

# Display the first few rows of the result
print(average_doubling_time.head())

# Some interesting details in the data:
# Albania shows a negative doubling time (-202.6), indicating either population decline or data issues.

# - Countries with 'Fast Doubling' time might have high population growth rates or recent economic changes.
# - Countries with 'Slow Doubling' time might have aging populations or low birth rates or they may be facing economic or social challenges.
# - Countries with 'Medium Doubling' might have steady population growth, often seen in developing nations.

# Limitations when working with population data: 
# 1) Data quality issues, missing values, population estimates, and assumptions, etc.
# 2) Lagging or limited time series - For example, in case of India, there were provided irregular time intervals as we have seen with visuals also.
#   This can affect the accuracy of growth rate calculations and predictions.
# 3) Population growth is a complex phenomenon influenced by various factors like birth rates, death rates, migration, and government policies.
# But we do not have such data in this dataset. 
# 4) Using of Rule of 70 is simplification and may not be accurate for all countries or time periods.
# 5) Subjectivity in Clustering (Just my funny categorization) - The categories of 'Fast', 'Medium', and 'Slow' doubling times are arbitrary.

