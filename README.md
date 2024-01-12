# Morningstar-scraping
This program search the Morningstar website and finds stocks that have more than 15% return, based on their fair value estimate. You should have premium membership. 

The code you is an extensive script for web scraping financial information from the Morningstar website using Selenium and BeautifulSoup. Before running this code, please ensure you have the required dependencies installed, such as Selenium, BeautifulSoup, and a suitable web driver ( ChromeDriver).

To execute the code, you need to provide the required inputs when prompted. Here's a summary of the inputs:

input1: Your Morningstar login email

input2: Your Morningstar login password

input3: Market selection, there are 3 options: ("NASDAQ", "NYSE", "LSE")

input4: Morningstar rating selection, , there are 4 options: ("stars_all", "stars_5", "stars_4", "stars_3")

input5: Time (in seconds) to sleep before interacting with the page (TS_value)

input6: WebDriverWait time (in seconds) for explicit waits (wait_val)


After providing these inputs, the script will navigate through the Morningstar website, login, choose market and rating, extract information for each stock, and save the results to a CSV file.


Here's a list of the main libraries and modules that were used, you may need to install some of them:

bs4 (Beautiful Soup): A library for web scraping purposes.

time: A standard Python library for handling time-related operations.

requests: A library for making HTTP requests.

selenium: A web testing library that is often used for web scraping, particularly when dealing with dynamic content.

pandas: A powerful data manipulation library for working with structured data.

csv: A built-in Python module for working with CSV files.

datetime: A module for working with dates and times.

tkinter: A standard Python library for creating graphical user interfaces (GUIs).


Note: Running web scraping scripts may violate the terms of service of the website. Ensure you comply with the website's terms and conditions, and consider checking their robots.txt file to see if web scraping is allowed.
