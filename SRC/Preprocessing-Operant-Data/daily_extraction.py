from lga_sha_extract_refactor import lga_sha_extract_refactor
from pr_extract_refactor import pr_extract_refactor
from shock_extract_refactor import shock_extract_refactor

import glob
import os

'''
    This file is to extract new raw data that is generated from the experiments.
    Compare against existing output file names to identify which (new) raw files to process

'''

def daily_extraction():

    lga_files_paths, sha_files_paths, pr_files_paths, shock_files_paths = [], [], [], []

    output_dir_path = 				### fill the path of where the excel_output_files should be stored
    input_dir_path = 				### fill the path of where the raw data is uploaded and stored 


    # 
    output_files = [os.path.basename(file).split('_')[0] for file in glob.glob(output_dir_path + '/**/**/*.xlsx')]
    output_files_test = [os.path.basename(file).split('_')[0] for file in glob.glob(output_dir_path + '/*.xlsx')]
    input_files_name_path = [(os.path.basename(file), file) for file in glob.glob(input_dir_path + '/**/*')]

    print(input_files_name_path)

    for tuple_name_path in input_files_name_path:
        filename = tuple_name_path[0]
        filepath = tuple_name_path[1]

        # If the filename is not in output files, this means that the raw file is "new" (hasn't been processed before)
        # Add to a list to then process it after
        if filename not in output_files:
            filename_lower = filename.lower()
            if 'lga' in filename_lower or 'pretreatment' in filename_lower:
                lga_files_paths.append(tuple_name_path)
            elif 'sha' in filename_lower or 'dissection' in filename_lower:
                sha_files_paths.append(tuple_name_path)
            elif 'shock' in filename_lower:
                shock_files_paths.append(tuple_name_path)
            elif 'treatment' in filename_lower or 'pr' in filename_lower:
                pr_files_paths.append(tuple_name_path)
    
    lga_sha_extract_refactor(lga_files_paths)
    print(lga_files_paths)
    lga_sha_extract_refactor(sha_files_paths)
    print(sha_files_paths)
    pr_extract_refactor(pr_files_paths)
    print(pr_files_paths)
    shock_extract_refactor(shock_files_paths)
    print(shock_files_paths)
    print('Daily extraction script ending')

daily_extraction()