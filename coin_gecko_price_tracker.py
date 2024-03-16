#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 23:07:31 2024

@author: erikware
"""

import requests
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', \
                    filename='price_tracker.log', filemode='w')

# Member Functions
def call_api(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()  # Return JSON response
        else:
            logging.error("Error: %s", response.status_code)
            return None
    except Exception as e:
        logging.error("Error: %s", e)
        return None
    
def write_to_csv(data_frame, file_path):
    try:
        # Write DataFrame to CSV file
        data_frame.to_csv(file_path, index=False)
        logging.info("DataFrame has been written to %s", file_path)
    except Exception as e:
        logging.error("Error: %s", e)

def read_from_csv(file_path):
    try:
        # Read CSV file into DataFrame
        data_frame = pd.read_csv(file_path)
        return data_frame
    except Exception as e:
        logging.error("Error: %s", e)
        return None

    
# Output data to csv
def write_grouped_rows_to_csv(data_frame, column_name, output_directory):
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        
        # Group DataFrame by the specified column
        grouped = data_frame.groupby(column_name)

        # Iterate through each group
        for group_name, group_data in grouped:
            # Create file path for the group
            file_path = os.path.join(output_directory, f"{group_name}.csv")

            # Write group data to CSV file, append if file exists
            mode = 'a' if os.path.exists(file_path) else 'w'
            
            group_data.to_csv(file_path, mode=mode, index=False, header=not os.path.exists(file_path))
            logging.info("Data for %s written to %s", group_name, file_path)

    except Exception as e:
        logging.error("Error: %s", e)

        
# Main
def main():
    # Set API Request
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    params = {"vs_currency": "USD", 
              "per_page": "250", 
              "page": "1", 
              "sparkline": "false", 
              "locale": "en" }
    
    headers = {"x-cg-demo-api-key": "CG-XAmtVYTcdRYK14aDdS2egGY9"}
    
    # use test data
    use_test_data = False
    
    # Execute API call and parse data
    try:
        # execute URL request and get coin data
        if use_test_data == False:
            coin_list_json = call_api(url, params, headers)
            coin_data_df = pd.DataFrame(coin_list_json)
            
            write_to_csv(coin_data_df, "test_csv_out.csv")
        else:
            coin_data_df = read_from_csv("test_csv_out.csv")
        
        # Specify the column to group by
        group_column = "symbol"
    
        # Specify the output directory
        output_directory = "coin_files"
        
        # Create output files
        write_grouped_rows_to_csv(coin_data_df, group_column, output_directory)
    except Exception as e:
        logging.error("Error: %s", e)
    


if __name__ == "__main__":
    main()
    logging.shutdown() 
