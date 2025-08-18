# Preprocessing Operant Data

This project focuses on preprocessing operant conditioning experimental data.

## Overview

This tool processes raw data from operant conditioning experiments to prepare it for analysis. It handles data cleaning, formatting, and basic statistical calculations.

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
