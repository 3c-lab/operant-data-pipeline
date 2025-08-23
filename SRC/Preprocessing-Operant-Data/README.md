## README

MedPC session TXT files are automatically converted into a custom Excel output file using the open-source extraction tool for Med-PC data, [GEToperant] (https://github.com/George-LabX/GEToperant), code from which can be found in the **getoperant_source folder**, profiles for it are in the **getoperant_profiles folder**

Khoo, S. Y. (2021). GEToperant: A General Extraction Tool for Med-PC Data. Figshare. doi: 10.6084/m9.figshare.13697851

The **daily_extraction.py** code identifies the new raw files from the raw data folder on Dropbox, where data generated from the experiments is uploaded, by comparing it against existing output file names and then processes it using the appropriate **refactor.py** code

