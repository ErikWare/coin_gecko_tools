#!/bin/bash


# Loop to run the script four times
for i in {1..4}; do
    # Echo starting message
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Starting script iteration $i..."
    
    # Run your Python script
    python coin_gecko_price_tracker.py --page $i
    
    # Echo completion message
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Script iteration $i completed."
    
    # Wait for one second before the next call
    sleep 1
done