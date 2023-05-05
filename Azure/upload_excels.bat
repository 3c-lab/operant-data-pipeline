@echo off
azcopy copy "C:\Users\yunyi\OneDrive\Desktop\azcopy_test\LGA\*" "https://datalakegltest.blob.core.windows.net/containertest/input/LGA_general_coc" --recursive --overwrite=ifSourceNewer