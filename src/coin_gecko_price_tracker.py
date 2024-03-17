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
import datetime
import time

# Get current date and time
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Set up logging configuration with timestamp in the log file name
log_file_name = f"../logging/price_tracker_{current_time}.log"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', \
                    filename=log_file_name, filemode='w+')

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
  
        
# export to a parquet file, if the file exists add to it, otherwise create it
def to_parquet(df, file_path):

    # Check if file exists
    file_exists = os.path.exists(file_path)

    # Write DataFrame to Parquet file based on file existence
    if file_exists:
        existing_df = pd.read_parquet(file_path)
        pd.concat([existing_df, df], ignore_index=True).to_parquet(file_path)
    else:
        df.to_parquet(file_path)

        
# Main
def main():
    
    
    # Get static metadata
    # execution time
    #current_time
    
           
    # Specify the output directory
    output_data_path = "../data/coin_data.parquet"
    
    # Get meta data 
    try:
    
        # Set API Request
        url = "https://api.coingecko.com/api/v3/coins/markets"
        headers = {"x-cg-demo-api-key": "CG-XAmtVYTcdRYK14aDdS2egGY9"}
        
        coin_data_final_df = pd.DataFrame()
        
        # Hit Coin Gecko 4 times to get the top 1000 coins
        for i in range(4):
        
            page_num = i + 1
            
            # Set Params
            params = { "vs_currency": "USD", "per_page": 250, "page": page_num, "sparkline": False, "locale": "en" }
            
            # Request Coin Data
            logging.info("Request Coin data from CoinGecko API, page: %s", page_num)
            coin_list_json = call_api(url, params, headers)
            
            # Convert the response to dataframe
            coin_data_results_df = pd.DataFrame(coin_list_json)
            
            # Append the existing dataframe
            coin_data_final_df = pd.concat([coin_data_results_df,coin_data_final_df], ignore_index=False)
            
            # Dont hit the API too fast
            time.sleep(1)

        # Data clense and enhancement
        coin_data_final_df['as_of_date'] = current_time
        coin_data_final_df = coin_data_final_df.drop('image', axis=1)
        coin_data_final_df = coin_data_final_df.sort_values(by='market_cap_rank')
             
        # Add to coin data set
        logging.info("Writing output parquet file: %s", output_data_path)
        to_parquet(coin_data_final_df, output_data_path)

        
    except Exception as e:
        logging.error("Error: %s", e)
    
    # Done
    logging.info("Success, Process Complete")


if __name__ == "__main__":
    main()
    logging.shutdown() 
