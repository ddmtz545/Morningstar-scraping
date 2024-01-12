# Morningstar-scrapping
This program search the Morningstar website and finds stocks that have more than 15% return, based on their fair value estimate

The code you is an extensive script for web scraping financial information from the Morningstar website using Selenium and BeautifulSoup. Before running this code, please ensure you have the required dependencies installed, such as Selenium, BeautifulSoup, and a suitable web driver ( ChromeDriver).

To execute the code, you need to provide the required inputs when prompted. Here's a summary of the inputs:

input1: Your Morningstar login email
input2: Your Morningstar login password
input3: Market selection, there are 3 options: ("NASDAQ", "NYSE", "LSE")
input4: Morningstar rating selection, , there are 4 options: ("stars_all", "stars_5", "stars_4", "stars_3")
input5: Time (in seconds) to sleep before interacting with the page (TS_value)
input6: WebDriverWait time (in seconds) for explicit waits (wait_val)

After providing these inputs, the script will navigate through the Morningstar website, login, choose market and rating, extract information for each stock, and save the results to a CSV file.

Note: Running web scraping scripts may violate the terms of service of the website. Ensure you comply with the website's terms and conditions, and consider checking their robots.txt file to see if web scraping is allowed.
