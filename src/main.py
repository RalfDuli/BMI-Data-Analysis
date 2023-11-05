import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def find_BMI(height, weight):
    output = weight / (height*height)
    pd.set_option('display.max_rows', None)
    print(output)
    return output 

def clean_data():
    # Reading the Excel sheets as Pandas DataFrames.
    form_1_df = pd.read_excel('data/GROUP PROJECT DATA (2021-24).xlsx', sheet_name='FORM 1')
    form_2_df = pd.read_excel('data/GROUP PROJECT DATA (2021-24).xlsx', sheet_name='FORM 2')

    # Filtering the DataFrames by height, body mass and MET.min.wk values.
    form_1_df_cleaned = form_1_df[['Height (m):', 'Body Mass (kg):', 'IPAQ MET.min.wk-1']].dropna()
    form_2_df_cleaned = form_2_df[['Height (m):', 'Body Mass (kg):', 'IPAQ MET.min.wk-1']].dropna()

    # Filtering out units of measurements from the DataFrames, isolating the numeric components.
    form_1_df_cleaned['Height (m):'] = form_1_df_cleaned['Height (m):'].astype(str).str.replace('m','').astype(float)
    form_2_df_cleaned['Height (m):'] = form_2_df_cleaned['Height (m):'].astype(str).str.replace('m','').astype(float)
    form_1_df_cleaned['Body Mass (kg):'] = form_1_df_cleaned['Body Mass (kg):'].astype(str).str.replace('kg','').astype(float)
    form_2_df_cleaned['Body Mass (kg):'] = form_2_df_cleaned['Body Mass (kg):'].astype(str).str.replace('kg','').astype(float)

    # Normalizing height measurements for those who inputted their height in centimetres.
    form_1_df_cleaned.loc[form_1_df_cleaned['Height (m):'] > 10, 'Height (m):'] /= 100
    form_2_df_cleaned.loc[form_2_df_cleaned['Height (m):'] > 10, 'Height (m):'] /= 100

    # Adding a new column to the DataFrames, BMI.
    heights_form_1 = form_1_df_cleaned['Height (m):']
    body_masses_form_1 = form_1_df_cleaned['Body Mass (kg):']
    form_1_df_cleaned['BMI'] = find_BMI(heights_form_1, body_masses_form_1)

    heights_form_2 = form_2_df_cleaned['Height (m):']
    body_masses_form_2 = form_2_df_cleaned['Body Mass (kg):']
    form_2_df_cleaned['BMI'] = find_BMI(heights_form_2, body_masses_form_2)

    # Stripping the cleaned DataFrames of unneccessary attributes.
    form_1_df_cleaned = form_1_df_cleaned[['BMI', 'IPAQ MET.min.wk-1']]
    form_2_df_cleaned = form_2_df_cleaned[['BMI', 'IPAQ MET.min.wk-1']]

    # Sorting the DataFrames by BMI in ascending orders.
    form_1_df_cleaned = form_1_df_cleaned.sort_values(by='BMI', ascending=True)
    form_2_df_cleaned = form_2_df_cleaned.sort_values(by='BMI', ascending=True)

    # Output a list of both cleaned DataFrames.
    output = [form_1_df_cleaned, form_2_df_cleaned]
    return output

def plot_data(df):
    bmi_data = df['BMI']
    met_data = df['IPAQ MET.min.wk-1']

    # Plot a scatter plot of the BMI and MET.min per week data.
    plt.xlabel('BMI')
    plt.ylabel('MET.min per week')
    plt.scatter(bmi_data, met_data)

    # Plot a line of best fit and title the plot with
    # the slope and the intercept of the line of best fit.
    slope, intercept = np.polyfit(bmi_data, met_data, 1)
    regression_function = slope * bmi_data + intercept
    plt.title(f'Slope={round(slope,2)}, Intercept={round(intercept,2)}')
    plt.plot(bmi_data, regression_function, color='r')

    plt.show()
    

def main():
    form_1_df, form_2_df = clean_data()
    plot_data(form_1_df)
    plot_data(form_2_df)

if __name__ == '__main__':
    main()