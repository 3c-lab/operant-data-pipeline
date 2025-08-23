from getoperant import GEToperant as getop 
from openpyxl import Workbook
import openpyxl
import os

'''
    The function has two parameters: lga_files and sha_files
    Both parameters are lists of files of its respective experiment type that are to be processed
    
'''

def pr_extract_refactor(extract_filepaths):

    print('PR_EXTRACTING')

    for tuple_name_path in extract_filepaths:

        filename = tuple_name_path[0]

        filename_path = tuple_name_path[1]

        filename_lower = filename.lower()

        if 'oxy' in filename_lower:
            drug_folder, exp_folder = 'OXYCODONE', 'PR'
        else:
            drug_folder, exp_folder = 'COCAINE', 'PR'
        
        # Uses the profile from GEToperantShA.xlsx        
        profile_file_name = 'C:/Users/georg/George Lab Dropbox/George_Lab/Experiments/DataStream/DataSource/data_automation/getop_profiles/pr_getop_profile.xlsx'        
        
        # Testing on personal computer
        # profile_file_name = '/Users/haltand/George Lab Dropbox/George_Lab/Experiments/DataStream/DataSource/data_automation/getop_profiles/pr_getop_profile.xlsx'        

        # Arguments for GEToperant function
        medpc_test_files = [filename_path]
        output_file_name = f'{filename}_output.xlsx'

        # TODO: Create a subdirectory for each individual output
        output_filepath = f'C:/Users/georg/George Lab Dropbox/George_Lab/Experiments/DataStream/DataSource/excel_output_files/{drug_folder}/{exp_folder}/{output_file_name}'
        azure_output_filepath = f'C:/Users/georg/George Lab Dropbox/George_Lab/Experiments/DataStream/DataSource/azure_excel_output_files/{drug_folder}/{exp_folder}/{output_file_name}'

        # TODO: Currently used with manual_file_extraction as the filepath for the user changes
        # Testing on personal computer
        # output_filepath = f'/Users/haltand/George Lab Dropbox/George_Lab/Experiments/DataStream/DataSource/excel_output_files/{drug_folder}/{exp_folder}/{output_file_name}'
        # azure_output_filepath = f'/Users/haltand/George Lab Dropbox/George_Lab/Experiments/DataStream/DataSource/azure_excel_output_files/{drug_folder}/{exp_folder}/{output_file_name}'

        # Remove files if they exist to rerun script with new output
        if os.path.exists(output_filepath):
            os.remove(output_filepath)
            print('Old file deleted')
        else:
            print('No file to delete', output_filepath)

        if os.path.exists(azure_output_filepath):
            os.remove(azure_output_filepath)
            print('Old file deleted')
        else:
            print('No file to delete', azure_output_filepath)

        # Get rid of the period at end of file possibly causing issue with getoperant
        with open(f"{filename_path}", "r+") as fp:

            lines = fp.readlines()

            if lines[-1] == '\x1a' or lines[-1] == '.':
            
                fp.writelines(lines[:-1])

            fp.close()

        # Figure out format to get more precise data into the spreadsheet
        getop.GEToperant(profile_file_name, medpc_test_files, output_filepath)
        getop.GEToperant(profile_file_name, medpc_test_files, azure_output_filepath)
        
        print('New file created at:', output_filepath)
        print('New file created at:', azure_output_filepath)
