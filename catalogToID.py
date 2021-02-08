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

for i in range(len(lines)):
    # Base URL for the search query
    URL = 'https://accessgudid.nlm.nih.gov/devices/search?query='

    # Append the catalog number to the base URL to form the completed URL
    URL += lines[catalog_numPos].strip()

    # The current catalog number being searched
    CAT_NUMBER = lines[catalog_numPos].strip()

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

    # Find all of the <a> tags within the search results section of the webpage
    a_tags = searchResults.find_all('a')

    # Loop over each <a> tag and append each device number to the dev_IDs list
    for a in a_tags:
        if not (a.get('href')).startswith('#'):
            dev_IDs.append((CAT_NUMBER, a.get('href').strip('/devices/')))

# Remove duplicate device identifiers and maintain the ordering 
dev_IDs = [i for n, i in enumerate(dev_IDs) if i not in dev_IDs[:n]]

# Create pandas data frame    
df = pd.DataFrame(dev_IDs, columns=['Catalog Number', 'Device Identifier'])

# Write relevant data to an Excel file
df.to_excel('output.xlsx', index=False, freeze_panes=(1,0))

# Close the text file
catalog_nums.close()
