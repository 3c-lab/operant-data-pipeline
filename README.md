# operant-data-pipeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


This repository is the code and guidelines associated with the manuscript:

**Title:** *Automated pipeline for operant behavior phenotyping for high-throughput data management, processing, and visualization*

**Authors:** 
Sunwoo Kim, BSc<sup>#</sup>; 
Yunyi Huang, MSc<sup>#</sup>; 
Uday Singla<sup>#</sup>; 
Andrew Hu, BSc; 
Sumay Kalra, BSc; 
Alex A. Morgan, BSc; 
Benjamin Sichel, BSc; 
Dyar Othman, BSc; 
Olivier George, PhD; 
Lieselot L.G. Carrette, PhD<sup>*</sup>

<sup>#</sup>These authors contributed equally.  
<sup>*</sup>Corresponding author: lcarrette@health.ucsd.edu.

**Abstact:** Operant behavior paradigms are essential in preclinical models of neuropsychiatric disorders, such as substance use disorders, enabling the study of complex behaviors including learning, salience, motivation, and preference. These tasks often involve repeated, time-resolved interactions over extended periods, producing large behavioral datasets with rich temporal structure. To support genome-wide association studies (GWAS), we have phenotyped over 3,000 rats for oxycodone and cocaine addiction-like behaviors using extended access self-administration, producing over 100,000 data files. To manage, store, and process this data efficiently, we leveraged Dropbox, Microsoft Azure Cloud Services, and other widely available computational tools to develop a robust, automated data processing pipeline. Raw MedPC operant output files are automatically converted into structured Excel files using custom scripts, then integrated with standardized experimental, behavioral, and metadata spreadsheets, all uploaded from Dropbox into a relational SQL database on Azure. The pipeline enables automated quality control, data backups, daily summary reports, and interactive visualizations. This approach has dramatically improved our high-throughput phenotyping capabilities by reducing human workload and error, while improving data quality, richness, and accessibility. We here share our approach, as these streamlined workflows can deliver benefits to operant studies of any scale, supporting more efficient, transparent, reproducible, and collaborative preclinical research.

## Citation
If you use this code (until the paper above is published/this section updated), please cite the zenodo doi above

```bibtex
@article{kim2025,
  title={Automated pipeline for operant behavior phenotyping for high-throughput data management, processing, and visualization},
  author={Kim, Sunwoo and Huang, Yunyi and Singla, Uday and Hu, Andrew and Kalra, Sumay and Morgan, Alex A. and Sichel, Benjamin and Othman, Dyar and George, Olivier and Carrette, Lieselot L.G.},
  journal={Journal Name},
  year={2025},
  doi={10.XXXX/XXXXX}
}
```

## Workflow Diagram
![Figure 1: Pipeline overview](Figure%201.jpeg?raw=1)

The source code (**SRC**) folder contains the code for the different subsections:
- (1) **Preprocessing of operant data**: to extract data from raw MedPC files into structured excel output files
- (2) Integration with other data: does not have any code, but examples and template files are available in the **Templates** folder
- (3) **Combination in Relational Database**: to process excel output and other homogenized files, copy them over to azure and process on azure into a relational database
- (4) **Data Output and Visualization**:
  - Behavior Analysis Automation and Graph Generation: to generate a cohort behavior summary excel file and visual behavioral traces based on the excel output file, cohort information file, daily issues and exit file.
  - Interactive Visualization: to generate a web-based dashboard hosted via pythonanywhere providing real-time visualization of Excel output files
  - Backup database: to generate a CSV backup of the relational database from Azure to Dropbox using AzCopy
  - Tableau templates
 



