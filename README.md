# Objective

The main objective is to understand the entire process of a public procurement procedure, complying with the applicable legislation and considering potential political and social events that may directly influence behavioural patterns. 

In addition to these factors, there are errors made by both the contracting authority and the awarded entity.

There are also other factors that may influence these behaviours, provided by the data available on Portal Base, such as:
- the type of procedure (open tendering, restricted tendering, request for proposals, among others);
- the country district and municipality of execution;
- and the CPV, a code that represents the type of service contracted.

# Repository Structure

## File01_DownloadBaseGovData.py
To extract data within the download constraints, advanced filtering techniques were employed. 

The search interface of the base portal allows users to filter results not only by procedure type and contract date, but also by geographic criteria such as country, district, and municipality.

The data collection strategy involved systematically applying these filters in succession. 

For each year and month in the designated time frame, queries were executed separately for each contract type. 

For higher-density regions or periods, municipality-level filters were applied to reduce the number of results per query.

## File02_VerifyFilesWithMoreThan500Rows.py
## File03_DailyDownloadScript.py
If the number of results still exceeded the maximum allowable threshold of 500, the searches were further broken by day, effectively limiting each query to 24-hour periods.

## File04_VerifyMissingData.py
Once the initial download was completed, a verification script checked for missing file – those that had not been downloaded successfully due to connectivity issues – and re-initiated the download for any missing data.

## File05_VerifyEmptyFiles.py
Another script then scanned the dataset for empty files and identified those that contained only column headers without any contract records.

## File06_FixCSVFormatting.py
## File11_FixCSVFilesPerMonth.py
## File12_AggregateFilesPerTipo.py
One of the first issues encountered was inconsistency in the formatting of the raw CSV files, they were delimited by semicolons which is a common regional variant. 

Additionally, a subset of the files contained encoding errors, malformed characters, or partial rows, often due to variations in encoding between UTF-8 and Latin-1. To address these problems, a dedicated Python script was developed.

## File07_OrganizeFixedFiles.py
## File08_OrganizeFixedFilesByMonth.py
## File09_CreateFinalFilesPerMonth.py
The script processed files stored in a designated source folder and saved the corrected versions in a separate output directory. 

Logging was implemented to track each operation, capturing both successful files and files that raised decoding expressions. 

This logging was essential for transparency, error tracking, and reproducibility. Importantly, the script also avoided overwriting already corrected files, ensuring that previously cleaned data would not be redundantly processed or inadvertently modified.

## File10_DailyDownloadScriptByList.py
In cases where the portal returned an error during manual re-download – typically because the original information was not in the right format, a script generated series of individual daily queries to identify which contract was in error.

## File13_AddTipoDescription.py
During concatenation process, a new variable was introduced to each record, indicating the specific filter used during data extraction (e.g., the contract type or geographical level). 

This ensured that the contextual metadata from the original query was retained in the final dataset, supporting traceability and future disaggregation.

## File14_AggregateFilesPerCounty.py
Once the CSV files were successfully cleaned and re-encoded in UTF-8, they were reorganized into a consistent structure that mirrored their original filtering dimensions – by county.

## File15_AggregateFilesPerDistrict.py
Once the CSV files were successfully cleaned and re-encoded in UTF-8, they were reorganized into a consistent structure that mirrored their original filtering dimensions – by municipality district.

## File16_AggregateFilesPerMonth.py
A second set of scripts then concatenated individual files into aggregated monthly datasets.

## File17_AggregateFilesPerYear.py
Subsequent stages of the cleaning process focused on structured aggregation. 

The fixed monthly files were further merged to generate broader analytical dataset: one per type, one per county, one per district, and one per month. 

This multi-level structure enabled both special and temporal analysis, speed and ease of handling. 

At the end of this process, all data was aggregated by year, producing one master file for each year between 2015 and 2024. These annual files included a comprehensive set of variables describing the contract value, contracting authority, supplier, procedural method, geographic location, and relevant dates.

## File18_DeleteWrongYears.py
To facilitate the automation of monthly queries on the base portal, the data extraction process was initially designed to fetch contract records from the first day of each month to the first day of the following month. 

This approach simplified the coding logic by maintaining uniform start and end points for all time ranges. 

However, an important peculiarity of the portal’s behavior became apparent: results from the first day of the year were incorrectly included in the dataset to the preceding year (as well as in the correct year). 

To resolve this overlap and ensure temporal accuracy, a post-processing script was implemented that filtered each file to retain only those records whose contract date strictly belonged to the intended year. 

## File19_JupyterLab_CPV_study.ipynb
Of the 30 434 CPV codes analyzed, 222 were selected. From the 222 selected cases, regardless of the type of contract (e.g., service acquisition, public service concessions, others), there are 112 distinct final CPVs. The Jupyter Lab code and the final complete list of selected codes can be consulted here.

## File20_JupyterLab_DataCleaning.ipynb
During the cleaning stage, features with generic object data type were converted to more appropriate types such as datetime for date fields and float for monetary values, improving consistency and enabling more efficient downstream processing. 

Additionally, new features were created from logical transformations and pattern extraction, such as splitting the NIPC and entity name, which were originally stored together in the same field for both awarding and awarded entities. 

This separation enabled more accurate entity-level analysis and easier cross-referencing with external datasets, such as CPV catalogs or fiscal registries. 

## File21_JupyterLab_CPVwithDictionaryOfTerms.ipynb
In order to strengthen the selection of the appropriate CPV codes, a dictionary of terms was created and used to search for CPVs based on the contract object and awarding entity. 

It was found that 101 codes appeared in both lists, 11 only in the manually selected list, and 4240 exclusively in the list obtained through the term dictionary search. 

The 11 codes present solely in the manual list were retained, as they refer to specific medical practices not included in the dictionary, such as homeopathy, urology, or medical imaging. 

The 4240 codes identified exclusively through the dictionary search mostly relate to procedures involving public health entities but not directly linked to healthcare provision – for example, facility maintenance or furniture acquisition. 






