## README

MedPC session TXT files are automatically converted into a custom Excel output file using the open-source extraction tool for Med-PC data, [GEToperant] (https://github.com/George-LabX/GEToperant), code from which can be found in the **getoperant_source folder**, profiles for it are in the **getoperant_profiles folder**

Khoo, S. Y. (2021). GEToperant: A General Extraction Tool for Med-PC Data. Figshare. doi: 10.6084/m9.figshare.13697851

Several times per day, using task scheduler, the **daily_extraction.py** code is run to identify new raw files in the raw data folder on Dropbox, where data generated from the experiments is uploaded, by comparing against existing output file names and then the new data identified is processed using the appropriate **refactor.py** code for the session type.

![Figure 2](https://github.com/user-attachments/assets/308cc37e-79da-447f-98f0-6b8f61dad7ee)