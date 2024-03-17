#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:50:41 2024

@author: erikware
"""

import argparse
import requests
import pandas as pd
import os
import logging
import datetime

# Set up logging
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_name = f"../logging/analize_market_cap_change{current_time}.log"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', \
                    filename=log_file_name, filemode='w+')

# Member Functions
def read_parquet_to_dataframe(file_path):
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Read Parquet file into DataFrame
        df = pd.read_parquet(file_path)
        logger.info("DataFrame successfully read from Parquet file.")
        return df
    
    except Exception as e:
        logger.error(f"Error reading Parquet file: {e}")
        return None
        
# Main
def main():
    
   
    # Log the input arguments and indicate that the program is being executed
    logging.info("analize_market_cap_change() is executing")
    
    # Execute API call and parse data
    try:
        # execute URL request and get coin data
       
        # Specify the output directory
        input_data_path = "../data/coin_data.parquet"
        
        # Add to coin data set
        logging.info("cread coin parquet data set: %s", input_data_path)
        coin_data_df = read_parquet_to_dataframe(input_data_path)
        
    except Exception as e:
        logging.error("Error: %s", e)
        

    # do some data science!!!
    
    try:
        # get distinct list of symbols
        distinct_values = coin_data_df['column_name'].unique()
        
        #For Each symbol perform find the market cap change over time
        selected_rows_df = df[df['category'] == 'A']
        
    except Exception as e:
        logging.error("Error: %s", e)
    
    # Done
    logging.info("Success, analize_market_cap_change() complete" )


if __name__ == "__main__":
    main()
    logging.shutdown() 














