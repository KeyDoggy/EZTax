# About

EZTax was created to solve a simple, yet time consuming problem; US sales taxes. In the United States, sales tax can be broken down into state tax and county tax. 
When companies complete thousands of transactions per month, it becomes incredibly time consuming to manually calculate which county every sale corresponds to.
EZTax uses html parsing to extrapolate which county each sale is attributable to, and the tax due for each sale. It then uses Pandas dataframes to condense the 
information into an easy to read excel workbook.

# Features

- Find out what state and county your sale took place in
- Find out the tax payable per sale
- Write all of this information into an organized excel file

# Setup

Users must download the following file and install the following libraries:

- pandas
- urllib.request
- HTMLTableParser
- pprint
- tax_rates.py

# Users must set up their excel file as follows
- Have at least 3 columns named exactly: "Time" "ZIP" "Pre Tax Sales"
- Time column should be dates
- ZIP column should be ZIP codes in the format 12345 or 12345-7890
- All columns should be the same length

Change the variable DATA_NAME to be the name of your excel file exactly. Eg: DATA_NAME = "CO Sales 2023.xlsx"
Change the variable OUTPUT_NAME to be the desired name of the output file exactly. Eg: OUTPUT_NAME = "CO Sales 2023 vTax.xlsx"

Ensure the excel file and tax_rates.py are in the same directory as EZTax.py. Run the file and when finished, download the new excel for access.

# Tools Used

- Pandas
- Request
- HTMLTableParser
- Pprint

# Websites Used
- https://www.sales-taxes.com/
- https://www.getzips.com/zip
