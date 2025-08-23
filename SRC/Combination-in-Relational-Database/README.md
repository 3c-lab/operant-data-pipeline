
# Combination in Relational Database

![Figure 4](Figure%204.jpeg)

Several steps are followed to generate a relational database

- **Automated-copy**: data is copied over from Dropbox to Azure Datalake using AzCopy scheduled with Microsoft Task Scheduler
- **Automated-processing**: data is processed in Azure (code loaded in the Azure Databricks, automatically scheduled through Azure Data Factory, and once processed automatically integrated in an Azure SQL database (as shown in the Azure Data Factory screenshot below.
- **Automated_Combination**: combines all tables of the relational database in a single combined table (discarding data after last good session for exits or data from faulty sessions for issues), which is the raw database. These 3 steps all proceed daily automated.




![Azure_Screenshot](Azure_Screenshot.png)


- **Stable_Calculations**: a selection of the data can be taken, data discarded according to additional quality criteria, data imputated, and dependent measures calculated. This is done by calling this function periodically and manually, so this database is "stable" in between these runs. 
