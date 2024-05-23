import pandas as pd

def process_and_save_temperature_data():
    try:
        df = pd.read_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\modified_data_15min.csv')
        df_extracted = df[['RoundedDateTime', 'Zone', 'Subzone', 'Temp']]
        df_pivoted = df_extracted.pivot_table(index=['RoundedDateTime'], columns=['Zone', 'Subzone'], values='Temp')
        df_pivoted['Mean zone B'] = (df_pivoted[('B', 1)] + df_pivoted[('B', 2)]) / 2
        df_pivoted['Mean zone C'] = (df_pivoted[('C', 1)] + df_pivoted[('C', 2)]) / 2
        df_pivoted = df_pivoted.round(2)
        df_pivoted.reset_index(inplace=True)
        df_pivoted.columns = ['date', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']
        df_pivoted[['date', 'time']] = df_pivoted['date'].str.split(expand=True)
        df_pivoted = df_pivoted[['date', 'time', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']]
        df_pivoted.to_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\mean_Temperature_data.csv', index=False)
        print("Temperature data processed and saved successfully.")
    except Exception as e:
        print(f"Error processing temperature data: {e}")

def process_and_save_par_data():
    try:
        df = pd.read_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\modified_data_15min.csv')
        df_extracted = df[['RoundedDateTime', 'Zone', 'Subzone', 'PAR']]
        df_pivoted = df_extracted.pivot_table(index=['RoundedDateTime'], columns=['Zone', 'Subzone'], values='PAR')
        df_pivoted['Mean zone B'] = (df_pivoted[('B', 1)] + df_pivoted[('B', 2)]) / 2
        df_pivoted['Mean zone C'] = (df_pivoted[('C', 1)] + df_pivoted[('C', 2)]) / 2
        df_pivoted[df_pivoted < 0] = 0
        df_pivoted = df_pivoted.round(2)
        df_pivoted.reset_index(inplace=True)
        df_pivoted.columns = ['date', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']
        df_pivoted[['date', 'time']] = df_pivoted['date'].str.split(expand=True)
        df_pivoted = df_pivoted[['date', 'time', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']]
        df_pivoted.to_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\mean_PAR_data.csv', index=False)
        print("PAR data processed and saved successfully.")
    except Exception as e:
        print(f"Error processing PAR data: {e}")

def process_and_save_solar_radiation_data():
    try:
        df = pd.read_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\modified_data_15min.csv')
        df_extracted = df[['RoundedDateTime', 'Zone', 'Subzone', 'Solar radiation']]
        df_pivoted = df_extracted.pivot_table(index=['RoundedDateTime'], columns=['Zone', 'Subzone'], values='Solar radiation')
        df_pivoted['Mean zone B'] = (df_pivoted[('B', 1)] + df_pivoted[('B', 2)]) / 2
        df_pivoted['Mean zone C'] = (df_pivoted[('C', 1)] + df_pivoted[('C', 2)]) / 2
        df_pivoted[df_pivoted < 0] = 0
        df_pivoted = df_pivoted.round(2)
        df_pivoted.reset_index(inplace=True)
        df_pivoted.columns = ['date', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']
        df_pivoted[['date', 'time']] = df_pivoted['date'].str.split(expand=True)
        df_pivoted = df_pivoted[['date', 'time', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']]
        df_pivoted.to_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\mean_SolarRadiation_data.csv', index=False)
        print("Solar data processed and saved successfully.")
    except Exception as e:
        print(f"Error processing solar data: {e}")

def process_and_save_humidity_data():
    try:
        df = pd.read_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\modified_data_15min.csv')
        df_extracted = df[['RoundedDateTime', 'Zone', 'Subzone', 'Humidity']]
        df_pivoted = df_extracted.pivot_table(index=['RoundedDateTime'], columns=['Zone', 'Subzone'], values='Humidity')
        df_pivoted['Mean zone B'] = (df_pivoted[('B', 1)] + df_pivoted[('B', 2)]) / 2
        df_pivoted['Mean zone C'] = (df_pivoted[('C', 1)] + df_pivoted[('C', 2)]) / 2
        df_pivoted = df_pivoted.round(2)
        df_pivoted.reset_index(inplace=True)
        df_pivoted.columns = ['date', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']
        df_pivoted[['date', 'time']] = df_pivoted['date'].str.split(expand=True)
        df_pivoted = df_pivoted[['date', 'time', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']]
        df_pivoted.to_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\mean_Humidity_data.csv', index=False)
        print("Humidity data processed and saved successfully.")
    except Exception as e:
        print(f"Error processing humidity data: {e}")

def process_and_save_co2_conc_data():
    try:
        df = pd.read_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\modified_data_15min.csv')
        df_extracted = df[['RoundedDateTime', 'Zone', 'Subzone', 'CO2 conc']]
        df_pivoted = df_extracted.pivot_table(index=['RoundedDateTime'], columns=['Zone', 'Subzone'], values='CO2 conc')
        df_pivoted = df_pivoted.round(2)
        df_pivoted.reset_index(inplace=True)
        df_pivoted.columns = ['date', 'Zone B subzone 1', 'Zone C subzone 1']
        df_pivoted[['date', 'time']] = df_pivoted['date'].str.split(expand=True)
        df_pivoted = df_pivoted[['date', 'time', 'Zone B subzone 1',  'Zone C subzone 1']]
        df_pivoted.to_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\mean_CO2Conc_data.csv', index=False)
        print("CO2 data processed and saved successfully.")
    except Exception as e:
        print(f"Error processing CO2 data: {e}")

# Call each function to process and save the respective data
process_and_save_temperature_data()
process_and_save_par_data()
process_and_save_solar_radiation_data()
process_and_save_humidity_data()
process_and_save_co2_conc_data()
