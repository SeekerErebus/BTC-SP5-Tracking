#!/usr/bin/env python3
"""
Calculate 1-year, 2-year, and 4-year moving averages for S&P 500 data.
Input: JSON file with format [Year, Month, Price, Change, Percent]
Output: JSON file with format [Year, Month, MA1Y, MA2Y, MA4Y]
"""

import json
import sys
from collections import deque
from typing import List, Tuple, Optional

def calculate_moving_averages(data: List[List[float]]) -> List[List[float]]:
    """
    Calculate moving averages for S&P 500 price data.
    
    Args:
        data: List of [Year, Month, Price, Change, Percent]
    
    Returns:
        List of [Year, Month, MA1Y, MA2Y, MA4Y] starting from January 1874
    """
    # Sort data by year and month (should already be sorted, but ensure consistency)
    data.sort(key=lambda x: (x[0], x[1]))
    
    # Extract just the prices with their timestamps
    prices = [(int(row[0]), int(row[1]), float(row[2])) for row in data]
    
    # Find the starting index for January 1874
    start_idx = None
    for i, (year, month, _) in enumerate(prices):
        if year == 1875 and month == 1:
            start_idx = i
            break
    
    if start_idx is None:
        raise ValueError("Data does not contain January 1875")
    
    # Verify we have enough historical data for 4-year MA
    if start_idx < 47:  # Need 48 months (4 years) of prior data
        raise ValueError(f"Insufficient data before January 1875. Need 48 months, have {start_idx}")
    
    results = []
    
    # Process each month from January 1874 onward
    for i in range(start_idx, len(prices)):
        year, month, _ = prices[i]
        
        # Calculate 1-year MA (12 months)
        ma_1y = sum(prices[j][2] for j in range(i-11, i+1)) / 12
        
        # Calculate 2-year MA (24 months)
        ma_2y = sum(prices[j][2] for j in range(i-23, i+1)) / 24
        
        # Calculate 4-year MA (48 months)
        ma_4y = sum(prices[j][2] for j in range(i-47, i+1)) / 48
        
        results.append([year, month, ma_1y, ma_2y, ma_4y])
    
    return results

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Read input data
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Calculate moving averages
        results = calculate_moving_averages(data)
        
        # Write output data
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"Successfully processed {len(results)} months of data")
        print(f"Output written to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file - {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
