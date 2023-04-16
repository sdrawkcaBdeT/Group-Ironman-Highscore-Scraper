"""First attempt at building a python scraper for OSRS Group Ironman Highscores."""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the base URL and page range
base_url = "https://secure.runescape.com/m=hiscore_oldschool_ironman/group-ironman/?groupSize=4&page="
page_range = range(1, 22)

# Define the headers for our HTTP requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# Create an empty list to store the group data
group_data = []

# Loop over the page range and scrape the data from each page
for page_num in page_range:
    # Build the full URL for the current page
    url = base_url + str(page_num)
    
    # Send an HTTP GET request to the URL and get the page content
    response = requests.get(url, headers=headers)
    content = response.content
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(content, "html.parser")
    
    # Find the table that contains the player data and extract the rows
    table = soup.find("table", {"class": "uc-scroll__table"})
    rows = table.find_all("tr")
    
    # Add in a 1 second delay for each page to be kind and gentle
    time.sleep(1)
    
    # Loop over the rows and extract the player data
    for row in rows:
        # Extract the columns from the current row
        columns = row.find_all("td")
        
        # Check that there are 4 columns (Rank, Name, Level, Contributed EXP)
        if len(columns) == 4:
            # Extract the data from each column
            rank = columns[0].text.strip()
            name = columns[1].text.strip()
            level = columns[2].text.strip()
            xp = columns[3].text.strip()
            
            # Add the group data to the list
            group_data.append({"Rank": rank, "Name": name, "Level": level, "EXP": xp})
            
            # Create Pandas DataFrame from list of group data
            df = pd.DataFrame(group_data)
            

df