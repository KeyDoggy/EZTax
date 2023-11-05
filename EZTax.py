## Imports
import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
import pandas as pd
import tax_rates

## Excel file names
## File type must be an excel workbook ending in .xlsx
DATA_NAME = "CO Sales 2023.xlsx"
OUTPUT_NAME = "CO Sales 2023 vTax.xlsx"

## Opens a website and read its
## binary contents (HTTP Response Body)
def url_get_contents(url):

    # Opens a website and read its
    # binary contents (HTTP Response Body)

    #making request to the website
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    #reading contents of the website
    return f.read()

## Read data on the existing Excel file
data=pd.read_excel(DATA_NAME)

## Read variables and define lists for wanted outputs
state_list = []
time = data["Time"].tolist()
sales = data["Pre Tax Sales"].tolist()
zip_list = data["ZIP"].tolist()
county_list = []
combined_tax_payable = []
state_tax_payable = []
county_tax_payable = []
combined_tax =[]
state_tax = []
county_tax = []

## Look up each zip code for the county and add it to the list
for i in range(len(zip_list)):
    zip_code = str(zip_list[i])
    while len(zip_code) < 5:
        zip_code = "0"+zip_code
    if len(zip_code) > 5:
        zip_code = zip_code[:4]
    ## print(zip_code)   # To debug
    url = "https://www.getzips.com/cgi-bin/ziplook.exe?What=1&Zip="+zip_code+"&Submit=Look+It+Up.html"
    xhtml = url_get_contents(url).decode('utf-8')

    p = HTMLTableParser()

    p.feed(xhtml)

    df = pd.DataFrame(p.tables[2])

    if len(p.tables[2]) > 1:
        state = df.loc[1,1][len(df.loc[1,1])-2:]
        county = df.loc[1,2]+" County"

    ## To catch error with invalid zip code
    else:
        county = "Unknown"
        state = "Unknown"

    my_key = (state, county)

    ## Catch errors if the tax key doesn't have the county
    if((tax_rates.tax_guide.get(my_key)) is None):
        county_list.append("Error")
        state_tax_payable.append("Error")
        county_tax_payable.append("Error")
        combined_tax_payable.append("Error")
        state_tax.append("Error")
        county_tax.append("Error")
        combined_tax.append("Error")
        state_list.append("Error")
        continue

    county_list.append(county)
    state_tax_payable.append(sales[i]*tax_rates.state_rates.get(state))
    county_tax_payable.append(sales[i]*(tax_rates.tax_guide.get(my_key)-tax_rates.state_rates.get(state)))
    combined_tax_payable.append(tax_rates.tax_guide.get(my_key)*sales[i])
    state_tax.append(tax_rates.state_rates.get(state))
    county_tax.append(tax_rates.tax_guide.get(my_key)-tax_rates.state_rates.get(state))
    combined_tax.append(tax_rates.tax_guide.get(my_key))
    state_list.append(state)


## Create a data frame and export it to an excel file
excel = {"Date": time, "State":state_list, "Zip":zip_list, "County":county_list, "Pre-tax sales":sales, "State Tax Rate":state_tax, "State Tax Payable":state_tax_payable, "County Tax Rate":county_tax, "County Tax Payable":county_tax_payable, "Combined Tax Rate":combined_tax, "Combined Tax Payable":combined_tax_payable}
exceldf = pd.DataFrame(excel)
exceldf.to_excel(OUTPUT_NAME)