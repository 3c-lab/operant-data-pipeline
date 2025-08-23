
# Combination in Relational Database

![Figure 4](Figure%204.jpeg)

Several steps are followed to be able to generate a relational database

- **Input-Copy**: data is copied over from Dropbox to Azure Datalake using AzCopy
- **Input-processing**: data is processed for use on Azure (code loaded in the Azure Databricks, automatically scheduled through Azure Data Factory, and once processed it can then get automatically integrated in an Azure SQL database
![Azure_Screenshot](Azure_Screenshot.png)




This project demonstrates how to handle combinations in a relational database context.

## Problem Description

Given a table `Combinations` with two columns:
- `user_id`: The ID of the user
- `combination`: A string representing a combination

The goal is to find all valid combinations that meet certain criteria.

## Solution Approach

The solution uses SQL queries to:
1. Filter combinations based on specific conditions
2. Group and aggregate data as needed
3. Handle edge cases appropriately

## Features

- Data cleaning and validation
- Session data aggregation 
- Response rate calculations
- Time series formatting
- Export to analysis-ready formats

## Usage

1. Place raw data files in the `input` directory
2. Run the preprocessing script:
   ```
   python preprocess.py --input input_dir --output output_dir
   ```
3. Processed data will be saved to the specified output directory

## Output Format

The processed data includes:
- Cleaned session data
- Aggregated response metrics
- Time-stamped event sequences
- Summary statistics

## Requirements

- Python 3.7+
- pandas
- numpy
- scipy

