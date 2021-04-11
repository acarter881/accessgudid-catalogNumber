#! python3
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Reads each line of a text file as a catalog number
catalog_nums = open('list2.txt', 'r')
lines = catalog_nums.readlines()

# List for the device identifiers
dev_IDs = []

# Start reading from the first line of the text file
catalog_numPos = 0 

def companyNames():
    # Loop through the search results to find all of the Company Names
    for g in yo:
        try:
            if g.find('label', class_='device-attribute').text == 'Company Name:' and 'TYPE YOUR COMPANY NAME HERE' in g.text:
                howdy = g.text.strip().split('\n')[1].strip()
                choop.append(howdy)
        except AttributeError:
            pass

def deviceNumbers():
    # Create a counter variable for the position of the Company Name
    yurp = 0
    # Loop over each <a> tag and append each device number to the dev_IDs list
    for a in a_tags:
        try:
            if not (a.get('href')).startswith('#'):
                dev_IDs.append((CAT_NUMBER, a.get('href').strip('/devices/'), choop[yurp]))
                yurp += 1   
        except IndexError:
            pass

for i in range(len(lines)):
    # The current catalog number being searched
    CAT_NUMBER = lines[catalog_numPos].strip()

    # Base URL for the search query
    URL = 'https://accessgudid.nlm.nih.gov/devices/search?query='

    # Append the catalog number to the base URL to form the completed URL
    URL += CAT_NUMBER

    # Increment catalog_numPos, so the script goes to the next catalog number on its next iteration
    catalog_numPos += 1

    # Print information about the search to the terminal
    print(f'Searching for catalog number: {CAT_NUMBER}...')

    # Create the response object and check if the request is successful
    res = requests.get(URL)
    res.raise_for_status()

    # Create a soup object
    soup = BeautifulSoup(res.text, 'lxml')

    # Find the search results section of the webpage
    searchResults = soup.find(id='search-results-column')

    # Create an empty list for the Company Names
    choop = []

    # Create a variable for the main section of the webpage
    yo = searchResults.find_all('div', class_='xsmall-12 medium-6 columns')
    
    # If the find_all method returns an empty list, append to dev_IDs. Otherwise, call the companyNames function
    if yo == [] or soup.find_all('span', class_='spelling-correction'):
        dev_IDs.append((CAT_NUMBER, 'Not Found', 'Not Found'))
    else:
        companyNames()

    # Find all of the <a> tags within the search results section of the webpage
    a_tags = searchResults.find_all('a')

    # Call the deviceNumbers function
    if soup.find_all('span', class_='spelling-correction'):
        pass
    elif choop == []:
        dev_IDs.append((CAT_NUMBER, 'Not Found', 'Not Found'))
    else:
        deviceNumbers()

# Create pandas data frame
df = pd.DataFrame(data=dev_IDs, columns=['Catalog Number', 'Device Identifier', 'Company Name'])

# Write relevant data to an Excel file
df.to_excel(excel_writer='Output.xlsx', sheet_name='Medical Devices', index=False, freeze_panes=(1,0))

# Close the text file
catalog_nums.close()
