import pandas as pd
import numpy as np
import os
import plotly.express as px
from tqdm import tqdm  # Progress bar to track file processing
from datetime import datetime
    
# Path to your data folder
folder_path = './cleaned_dataset/data'
    
# Load metadata.csv
metadata_df = pd.read_csv('./cleaned_dataset/metadata.csv')
    
# Function to extract real and imaginary parts from complex impedance columns
import numpy as np
    
def extract_complex_parts(complex_series):
    # Initialize empty lists for real and imaginary parts
    real_part = []
    imag_part = []
    
    for x in complex_series:
        try:
            # Ensure x is a string and then evaluate it as a complex number
            if isinstance(x, str):
                x = eval(x)  # Evaluate the string as a Python expression

            # Check if x is a complex number, and if so, extract real and imaginary parts
            if isinstance(x, complex):
                real_part.append(np.real(x))
                imag_part.append(np.imag(x))
            else:
                # If x is not a complex number, append NaN (or handle as needed)
                real_part.append(np.nan)
                imag_part.append(np.nan)
        except Exception as e:
            # If an error occurs (e.g., invalid format), append NaN
            real_part.append(np.nan)
            imag_part.append(np.nan)
            print(f"Error processing value {x}: {e}")
        
    # Convert the lists to pandas Series and return them
    return pd.Series([real_part, imag_part], index=['real', 'imag'])
    
    
# Function to parse 'start_time' from list format to datetime
def parse_start_time(start_time_str):
    # Remove extra spaces and ensure proper formatting for list structure
    start_time_str = start_time_str.replace('  ', ',')  # Replace multiple spaces with commas
    start_time_str = start_time_str.replace(',,', ',')  # Remove consecutive commas
    
    # Handle cases where elements may be missing, for example, '2010.,7.,,,21.'
    start_time_str = '[' + ','.join(filter(None, start_time_str.split(','))) + ']'
    
    try:
        # Convert the cleaned-up string into a list
        start_time_list = eval(start_time_str)
    except:
        # If eval fails, return None or a default value
        return None
    
    # Ensure we have the correct number of elements in the list
    if len(start_time_list) != 6:
        return None
    
    # Extract individual components
    try:
        year = int(start_time_list[0])
        month = int(start_time_list[1])
        day = int(start_time_list[2])
        hour = int(start_time_list[3])
        minute = int(start_time_list[4])
        second = float(start_time_list[5])
    except ValueError:
        # If any conversion fails, return None or a default value
        return None
    
    # Construct a datetime object
    return datetime(year, month, day, hour, minute, int(second), int((second - int(second)) * 1e6))
    
# Function to load and process the data
def load_and_process_data():
    charge_discharge_data = []
    impedance_data = []
    
    # Loop through all the CSV files in the folder
    for i, row in tqdm(metadata_df.iterrows(), total=metadata_df.shape[0]):
        filename = row['filename']
        file_path = os.path.join(folder_path, filename)

        # Check if the file exists
        if os.path.exists(file_path):
            file_type = row['type']
    
            # For charge and discharge files
            if file_type == 'charge' or file_type == 'discharge':
                # Load charge/discharge data
                charge_discharge_df = pd.read_csv(file_path)
                    
                # Add metadata columns to charge/discharge dataframe
                charge_discharge_df['start_time'] = parse_start_time(row['start_time'])
                charge_discharge_df['ambient_temperature'] = row['ambient_temperature']
                charge_discharge_df['battery_id'] = row['battery_id']
                charge_discharge_df['test_id'] = row['test_id']
                charge_discharge_df['uid'] = row['uid']
                charge_discharge_df['Capacity'] = row['Capacity']
                charge_discharge_df['Re'] = row['Re']
                charge_discharge_df['Rct'] = row['Rct']
                
                charge_discharge_data.append(charge_discharge_df)
    
            # For impedance files
            elif file_type == 'impedance':
                # Load impedance data
                impedance_df = pd.read_csv(file_path)
                    
                # Add metadata columns to impedance dataframe
                impedance_df['start_time'] = parse_start_time(row['start_time'])
                impedance_df['ambient_temperature'] = row['ambient_temperature']
                impedance_df['battery_id'] = row['battery_id']
                impedance_df['test_id'] = row['test_id']
                impedance_df['uid'] = row['uid']
                impedance_df['Capacity'] = row['Capacity']
                impedance_df['Re'] = row['Re']
                impedance_df['Rct'] = row['Rct']
                    
                # Extract real and imaginary parts of impedance
                impedance_df['Battery_impedance_real'], impedance_df['Battery_impedance_imag'] = extract_complex_parts(impedance_df['Battery_impedance'])
                impedance_df['Rectified_Impedance_real'], impedance_df['Rectified_Impedance_imag'] = extract_complex_parts(impedance_df['Rectified_Impedance'])
                impedance_data.append(impedance_df)
    
    # Concatenate all the dataframes into single dataframes
    charge_discharge_df = pd.concat(charge_discharge_data, ignore_index=True)
    impedance_df = pd.concat(impedance_data, ignore_index=True)

    return charge_discharge_df, impedance_df
    
# Load and process the data
charge_discharge_df, impedance_df = load_and_process_data()


# Plot Battery Impedance (real part) from impedance_df
fig_impedance = px.line(impedance_df, x='test_id', y='Battery_impedance_real', 
                        title='Battery Impedance over Charge/Discharge Cycles',
                        labels={'test_id': 'Cycle Number', 'Battery_impedance_real': 'Battery Impedance (Ohms)'})
fig_impedance.show()

# Plot Electrolyte Resistance (Re) from charge_discharge_df and impedance_df
fig_Re = px.line(impedance_df, x='test_id', y='Re', 
                 title='Electrolyte Resistance (Re) over Charge/Discharge Cycles',
                 labels={'test_id': 'Cycle Number', 'Re': 'Re (Ohms)'})
fig_Re.show()

# Plot Charge Transfer Resistance (Rct) from charge_discharge_df and impedance_df
fig_Rct = px.line(impedance_df, x='test_id', y='Rct', 
                  title='Charge Transfer Resistance (Rct) over Charge/Discharge Cycles',
                  labels={'test_id': 'Cycle Number', 'Rct': 'Rct (Ohms)'})
fig_Rct.show()
