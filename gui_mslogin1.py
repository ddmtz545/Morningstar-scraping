import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv
import pandas as pd
from datetime import datetime

############numeric_value_ext extract the numeric value#########################
def numeric_value_ext(output):

    # Step 1: Remove non-numeric characters
    numeric_part = ''.join(char for char in output if char.isdigit() or char == '.')

    # Step 2: Convert the string to a numeric value (float)
    numeric_value = float(numeric_part)

    # Now, you can use the numeric_value for calculations
    return numeric_value

###################this function extracts price and etc.########################
def extract_ticker_info(driver):
    # Get the updated HTML content
    html_content = driver.page_source

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    try:
        fair_value_div = soup.find('div', {'id': 'FairValueEstimate', 'class': 'item'})
        price_div = soup.find('div', {'id': 'Price', 'class': 'item'})
        uncertainty_div = soup.find('div',{'id': 'Uncertainity', 'class': 'item'})
        economic_moat_div = soup.find('div', {'id': "EconomicMoat" })
        cost_allocation_div = soup.find('div', {'id':"Stewardship", 'class': 'item'})
        symbol_name_div = soup.find('div',{'id':"SnapshotTitle", 'class':"clearfix"})
        #financial_strenth_div = soup.find('div', {'id':"FinancialHealthGrade" , 'class': 'item'})
        #print(uncertainty_div)
        #print(fair_value_div)
        #type(fair_value_div)

        # Check if all div elements are found
        if all([fair_value_div,price_div,uncertainty_div,economic_moat_div,cost_allocation_div,symbol_name_div]):
            # Find the DataPoint tag within the div
            #datapoint tag should not have capital letters although in the html text it is DataPoint
            data_point = fair_value_div.find('datapoint')
            data_point_price = price_div.find('datapoint')
            data_point_uncertainty = uncertainty_div.find('datapoint')
            data_point_cost_allocation = cost_allocation_div.find('datapoint')
            data_point_EM = economic_moat_div.find('datapoint')
            symbol_dp = symbol_name_div.find('span',{'class':'securitySymbol'})
            name_dp = symbol_name_div.find('span',{'class':'securityName'})
            #data_point_FS = financial_strenth_div.find('img')

            # Check if the DataPoint tags are found
            if all([data_point,data_point_price,data_point_uncertainty,data_point_cost_allocation,data_point_EM,symbol_dp,name_dp]):
                # Extract the Fair Value Estimate value
                fair_value_estimate = data_point.text.strip()
                price=data_point_price.text.strip()
                uncertainty=data_point_uncertainty.text.strip()
                cost_allocation=data_point_cost_allocation.text.strip()
                economic_moat=data_point_EM .text.strip()
                symbol = symbol_dp.text.strip()
                name = name_dp.text.strip()


                # Display the extracted data
                print(f"Fair Value Estimate: {fair_value_estimate}")
                print(f"Price: {price}")
                print(f"Uncertainty: {uncertainty}")
                print(f"Cost Allocation: {cost_allocation}")
                print(f"Economic Moat: {economic_moat}")
                print(f"Security Name: {name}")
                print(f"Security Symbol: {symbol}")

                fair_value_estimate = numeric_value_ext(fair_value_estimate)
                price = numeric_value_ext(price)
                fpratio = fair_value_estimate/price
                fpratio_percent=((fair_value_estimate-price)/price)*100

                info_list=[fair_value_estimate,price,fpratio,fpratio_percent,uncertainty,cost_allocation,economic_moat,name,symbol]
                return info_list
            else:
                 print("DataPoint tags not found in one of the div elements.")
                 info_list = [0] * 7
                 return info_list
        else:
             print("One of the div elements not found.")
             info_list = [0] * 7
             return info_list
    except Exception as e:
           print(f"Error: {e}")
    info_list = [0] * 7
    return info_list
################################################################################

def run_program(input1, input2, input3, input4, input5, input6):
    # Replace this with your actual Python program logic
    result = f"Input 1: {input1}\nInput 2: {input2}\nInput 3: {input3}\nInput 4: {input4}\nInput 5: {input5}\nInput 6: {input6}"
    messagebox.showinfo("Program Result", result)
    print(input1,input2,input3,input4,input5,input6)
    

    userid = input1
    password = input2
    #"NASDAQ","NYSE","LSE
    # Choose the market (replace "NASDAQ" with the desired market name)
    selected_market = input3
    #"stars_all","stars_5" ,"stars_4" ,"stars_3"
    selected_msrating = input4
    ######wait time for page to load
    TS_value = numeric_value_ext(input5)   ##this values time.sleep
    wait_val = numeric_value_ext(input6)    ##vlue for wait = WebDriverWait(driver,3)

    # Set up the webdriver (choose the appropriate webdriver for your browser)
    driver = webdriver.Chrome()  # Change to webdriver.Firefox() if you're using Firefox
    # Navigate to the Morningstar website
    driver.get("https://www.morningstar.co.uk/uk/")
    time.sleep(TS_value)
    # Set up an explicit wait with a timeout of 10 seconds
    wait = WebDriverWait(driver,wait_val)

    ########Get rid of the  pop-ups including accept_cookies_button################

    try:
        #onetrust-accept-btn-handler
        myselector ='#onetrust-accept-btn-handler'
        accept_cookies_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, myselector)))
        accept_cookies_button.click()

    except TimeoutException:
        # If the button is not found within the specified time, handle it here
        print("Accept Cookies button not found within the specified time. Trying another selector.")
        try:
            accept_cookies_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[3]/div/div[1]/div/div[2]/div/button[3]")))
            accept_cookies_button.click()
        except TimeoutException:
               # If the button is not found within the specified time, handle it here
            print("Accept Cookies button not found within the specified time. Trying another XPath.")
            try:
                accept_cookies_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[3]/div/div[1]/div/div[2]/div/button[2]")))
                accept_cookies_button.click()
            except TimeoutException:
                  # If the button is not found within the specified time, handle it here
                print("Accept Cookies button not found within the specified time. Trying another XPath.")
                try:
                    accept_cookies_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div[3]/div/div[1]/div/div[2]/div/button[2]")))
                    accept_cookies_button.click()
                except TimeoutException:
                      # If the button is not found within the specified time, handle it here
                    print("Accept Cookies button not found within the specified time. Trying another XPath.")

        #########the xpath is variable in mac   reject        /html/body/div[7]/div[3]/div/div[1]/div/div[2]/div/button[2]
        #############accept                     /html/body/div[6]/div[3]/div/div[1]/div/div[2]/div/button[3]
        # Click the "Accept All Cookies" button
    time.sleep(TS_value)
    ####this is for "I'm an individual investor" button
    try:

        wait = WebDriverWait(driver, wait_val)
        # Wait for the "I'm an individual investor" button to appear
        individual_investor_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[7]/div[2]/div[2]/input[2]")))
        # Click the "I'm an individual investor" button
        individual_investor_button.click()

        # Now you can proceed with your other interactions on the webpage
    except Exception as e:
        print(f"Error: {e}")
    ################################################################################

    ########clicking on sign in
    # Identify and click on the link (replace with the actual attributes of your link)
    example_link = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[4]/div[3]/div/div/a[4]/span")))
    example_link.click()

    ####entering password and email
    # Identify and enter the email and password
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/ctrsi-signin-component/div/div/div[2]/main/section/div/div[2]/div/div/form/label[1]/input")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/ctrsi-signin-component/div/div/div[2]/main/section/div/div[2]/div/div/form/label[2]/div[2]/input")))

    email_input.send_keys(userid)  # Replace with your actual email
    password_input.send_keys(password)         # Replace with your actual password

    ######press sign in button

    example_link2 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/ctrsi-signin-component/div/div/div[2]/main/section/div/div[2]/div/div/form/div/button[2]/span")))
    example_link2.click()
    #wait = WebDriverWait(driver, wait_val)

    time.sleep(TS_value)
    # Set up an explicit wait with a timeout of 10 seconds
    wait = WebDriverWait(driver,wait_val)

    #################Click on five star stocks link########################################
    ############################### Identify and click on the link five star stocks
    stars_5_stocks = "/html/body/div[3]/div[1]/div/form/div[4]/div[2]/div[2]/div[3]/div/a"

    try :
        example_link3 = wait.until(EC.element_to_be_clickable((By.XPATH, stars_5_stocks)))
        example_link3.click()
    except TimeoutException:
        print("MS Research dropdown or option not found within the specified time.")


    # Assuming you have already identified the input box using its XPath
    time.sleep(TS_value)
    #############################Choosing the Market################################
    #######XPATH for Market box arrow
    dropdown_xpath = "/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ec-screener/ec-section/section/div/div/div/div/section/div/ec-container/div/div/div/section/div/div[1]/div/ec-section/section/div/div/div/ec-container/div/div/div/section/div/div/ec-section/section/div/div/div/ec-filters/div/form/ec-section/div/ec-container/div/div/div[2]/section/div/div/ec-section[1]/div/div/div/div/ec-combo-box/div/span/span[1]/span/span[2]"

    #######XPATH for NASDAQ
    #dropdown_xpath2 = "/html/body/span/span/span[2]/ul/li[2]"
    #selected_market = "NASDAQ"
    #######XPATH for NYSE
    #dropdown_xpath3 = "/html/body/span/span/span[2]/ul/li[3]"
    #selected_market = "NYSE"
    #######XPATH for LSE
    #dropdown_xpath4 = "/html/body/span/span/span[2]/ul/li[1]"
    #selected_market = "LSE"
    try:
        # Wait for the dropdown element to be clickable
        dropdown_element = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

        # Click on the dropdown to open the menu
        dropdown_element.click()

        # Dictionary with names as keys and XPaths as values
        dropdown_market_xpaths = {
        "NASDAQ": "/html/body/span/span/span[2]/ul/li[2]",
        "NYSE": "/html/body/span/span/span[2]/ul/li[3]",
        "LSE": "/html/body/span/span/span[2]/ul/li[1]"}

        # Choose the XPath based on the name
        # Choose the market (replace "NASDAQ" with the desired market name)
        #selected_market = "NASDAQ"
        selected_market_xpath = dropdown_market_xpaths.get(selected_market)

        #choose the Market XPATH ###########################################
        # Wait for the dropdown element to be clickable
        dropdown_element2 = wait.until(EC.element_to_be_clickable((By.XPATH, selected_market_xpath)))

        # Click on the dropdown to open the menu
        dropdown_element2.click()

    except TimeoutException:
        print("Market dropdown or option not found within the specified time.")
    ################################################################################

    time.sleep(TS_value)
    ###########################XPATH for MS Rating box##############################
    MSR_dropdown_XPATH= "/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ec-screener/ec-section/section/div/div/div/div/section/div/ec-container/div/div/div/section/div/div[1]/div/ec-section/section/div/div/div/ec-container/div/div/div/section/div/div/ec-section/section/div/div/div/ec-filters/div/form/ec-section/div/ec-container/div/div/div[3]/section/div/div/ec-section[1]/div/div/div/div/ec-combo-box/div/span/span[1]/span/span[2]"

    #MSR_dropdown_XPATH2 = "/html/body/span/span/span[1]/input"
    MSR_dropdown_XPATHs = {
    "stars_all":"/html/body/span/span/span[2]/ul/li[1]",
    "stars_5" : "/html/body/span/span/span[2]/ul/li[2]",
    "stars_4" : "/html/body/span/span/span[2]/ul/li[3]",
    "stars_3" : "/html/body/span/span/span[2]/ul/li[4]"
    }
    try :
        # Wait for the dropdown element to be clickable
        MSR_dropdown_element = wait.until(EC.element_to_be_clickable((By.XPATH, MSR_dropdown_XPATH)))
        # Click on the dropdown to open the menu
        MSR_dropdown_element.click()

        #selected_msrating = "stars_4"
        selected_rating_xpath = MSR_dropdown_XPATHs.get(selected_msrating)

        example_link3 = wait.until(EC.element_to_be_clickable((By.XPATH, selected_rating_xpath)))
        example_link3.click()
    except TimeoutException:
        print("MS Research dropdown or option not found within the specified time.")


    time.sleep(TS_value)
    ##############################number of rows in a page##########################
    #####select rows No.
    dropdown_element3 = wait.until(EC.element_to_be_clickable((By.XPATH,
    "/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ec-screener/ec-section/section/div/div/div/div/section/div/ec-container/div/div/div/section/div/div[2]/div/ec-section/section/div/div/div/ec-container/div/div/div/section/div/div[1]/ec-section/section/div/div/div/div/div/div[2]/ec-input/div/div/select")))

    # Create a Select object
    dropdown3 = Select(dropdown_element3)

    ### Select an option by visible text
    ###your options are: 10, 20, 50
    pagerows = "50"
    dropdown3.select_by_visible_text(pagerows)

    time.sleep(TS_value)
    ###################to extract the number of companies present in the search
    #Wait for the span element to be present (adjust the XPath accordingly)
    span_element = wait.until(EC.presence_of_element_located((By.XPATH,
    "/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ec-screener/ec-section/section/div/div/div/div/section/div/ec-container/div/div/div/section/div/div[2]/div/ec-section/section/div/div/div/ec-container/div/div/div/section/div/div[2]/ec-section/section/div/div/div/div/div/div/span"))
    )

    # Extract the text content of the span element
    text_content = span_element.text

    # Split the text using '/' and get the second part (index 1)
    desired_number = text_content.split('/')[1]

    # Print the result
    print('Number of companies:',desired_number)





    #########finding the weblink for search results:###############################################################
    '''
    current_url = driver.current_url
    driver.get(current_url)
    html_content = driver.page_source
    '''
    # (Optional) Add a delay to allow time for the page to load
    time.sleep(TS_value)
    # Set up an explicit wait with a timeout of 10 seconds
    wait = WebDriverWait(driver, wait_val)

    try:
        # Find all the links with the specified class
        #classname ='templates.hyperlink'
        classname ="mds-link mds-link--no-underline ec-table__investment-link ng-binding"
        # Specify the class name of the parent div
        #links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, classname)))

        # Constructing an XPath expression to find elements by class name
        xpath_expression = f"//*[contains(@class, '{classname}')]"
        # Find elements using XPath
        links = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
        #print(links)
        print("links list length1:",len(links))


        #print(links)
    ########################check links for None values s
        #myselector = '#ec-screener-table-securities-row-0 > td.ec-table__cell.ec-table__cell--data.mds-data-table__cell.ng-scope.ec-table__cell--sticky > div > span.ec-table-combined-key-field__name.ng-scope > a'
        #links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'myselector')))


        # Extract and visit each link
        i = 0
        # Initialize an empty list to store the results
        all_info_lists = []
        page_sources = []
        for link in links:
            try:
                href = link.get_attribute("href")
                print(f"Visiting link: {href}")
                i += 1

                # Open the link in a new tab
                driver.execute_script(f"window.open('{href}', '_blank');")

                # Switch to the newly opened tab
                driver.switch_to.window(driver.window_handles[-1])
                # Optionally, wait for the page to load, perform scraping, etc.
                time.sleep(TS_value)  # You can adjust the waiting time
                # Get the page source
                #msr_page_source = driver.page_source
                #click on the Morningstar Research tab
                # Identify and click on the link (replace with the actual attributes of your link)
            #try:
                # Find the link by ID
                link_MSR = driver.find_element(By.ID, 'LnkPage15')

                # Check if the link is present in the page source
                if link_MSR.is_displayed() and link_MSR.is_enabled() and 'Morningstar Research' in link_MSR.text:
                    print("MS Research link found, clicking on it...")
                    link_MSR.click()
                    ######extract specified info in extract_ticker_info() function
                    time.sleep(TS_value)
                    # Your existing code
                    #extract_ticker_info()
                    info_list = extract_ticker_info(driver)

                    if None in info_list or any(x is None for x in info_list):
                        print("Error: Some elements in info_list are None or NoneType.")
                    else:

                        current_url = driver.current_url
                        driver.get(current_url)
                        msr_page_source = driver.page_source
                        # Append the page source to the list
                        page_sources.append(msr_page_source)
                        # Append the info_list to the list
                        all_info_lists.append(info_list)
                        print('Number of link found with MS research:', i)

                else:
                    print("MS Research link is not present or not clickable.")

            except NoSuchElementException:
                    print(" MS Research link not found.")

            #time.sleep(TS_value)

            # Close the current tab
            driver.close()

            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])


        #####to go to next page if search results are >50
        if numeric_value_ext(desired_number)>50:
            counter = 0
            while True:
                counter += 1
                next_page_button = "/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ec-screener/ec-section/section/div/div/div/div/section/div/ec-container/div/div/div/section/div/div[2]/div/ec-section/section/div/div/div/ec-container/div/div/div/section/div/div[4]/ec-table/ec-section/section/div/div/div/ec-paginator[2]/ec-section/div/div/nav/ul/li[4]/a"
                next_page_button_link = wait.until(EC.element_to_be_clickable((By.XPATH, next_page_button)))
                next_page_button_link.click()
                time.sleep(TS_value)
                ##############################number of rows in a page##########################
                #####select rows No.
                dropdown_element3 = wait.until(EC.element_to_be_clickable((By.XPATH,
                "/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ec-screener/ec-section/section/div/div/div/div/section/div/ec-container/div/div/div/section/div/div[2]/div/ec-section/section/div/div/div/ec-container/div/div/div/section/div/div[1]/ec-section/section/div/div/div/div/div/div[2]/ec-input/div/div/select")))

                # Create a Select object
                dropdown3 = Select(dropdown_element3)

                ### Select an option by visible text
                ###your options are: 10, 20, 50
                pagerows = "50"
                dropdown3.select_by_visible_text(pagerows)

                time.sleep(TS_value)
                # Find elements using XPath
                links = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
                for link in links:
                    try:
                        href = link.get_attribute("href")
                        print(f"Visiting link: {href}")
                        i += 1

                        # Open the link in a new tab
                        driver.execute_script(f"window.open('{href}', '_blank');")

                        # Switch to the newly opened tab
                        driver.switch_to.window(driver.window_handles[-1])
                        # Optionally, wait for the page to load, perform scraping, etc.
                        time.sleep(TS_value)  # You can adjust the waiting time
                        # Get the page source
                        #msr_page_source = driver.page_source
                        #click on the Morningstar Research tab
                        # Identify and click on the link (replace with the actual attributes of your link)
                    #try:
                        # Find the link by ID
                        link_MSR = driver.find_element(By.ID, 'LnkPage15')

                        # Check if the link is present in the page source
                        if link_MSR.is_displayed() and link_MSR.is_enabled() and 'Morningstar Research' in link_MSR.text:
                            print("MS Research link found, clicking on it...")
                            link_MSR.click()
                            ######extract specified info in extract_ticker_info() function
                            time.sleep(TS_value)
                            # Your existing code
                            #extract_ticker_info()
                            info_list = extract_ticker_info()

                            if None in info_list or any(x is None for x in info_list):
                                print("Error: Some elements in info_list are None or NoneType.")
                            else:

                                current_url = driver.current_url
                                driver.get(current_url)
                                msr_page_source = driver.page_source
                                # Append the page source to the list
                                page_sources.append(msr_page_source)
                                # Append the info_list to the list
                                all_info_lists.append(info_list)
                                print('Number of link found with MS research:', i)

                        else:
                            print("MS Research link is not present or not clickable.")

                    except NoSuchElementException:
                            print(" MS Research link not found.")

                    #time.sleep(TS_value)

                    # Close the current tab
                    driver.close()

                    # Switch back to the original tab
                    driver.switch_to.window(driver.window_handles[0])

                if counter >= int(numeric_value_ext(desired_number)/50):
                    break

        print('Number of All links found:', i)
    except Exception as e:
        print(f"Error for links: {e}")





    ################################################################################
    ################################################################################
    ################################ Print or analyze the info_lists after the loop
    print(all_info_lists)
    for iteration, info_list in enumerate(all_info_lists):
        print(f"Iteration {iteration + 1}: {info_list}")

    # Save all_info_lists to a CSV file
    # Generate a timestamp for the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a CSV file name with the timestamp
    csv_file_path = f'all_info_lists_{selected_market}_{selected_msrating}_rows{pagerows}_{timestamp}.csv'

    # Save all_info_lists to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header (if applicable)
        csv_writer.writerow(['Fair_value_estimate', 'Price', 'FP_ratio', 'FP_ratio_percent', 'Uncertainty', 'cost_allocation', 'Economic_moat', 'Security_Name', 'Security_Symbol'])
        # Write each info_list to the CSV file
        csv_writer.writerows(all_info_lists)

    print(f"All info lists saved to: {csv_file_path}")

    # Optional: Read the CSV file into a pandas DataFrame for further analysis
    data = pd.read_csv(csv_file_path)
    print(data)
    #save  page_sources to a new csv file
    # Combine all page sources into a single string
    combined_page_sources = '<!--My_Unique_PAGE_DELIMITER-->'.join(page_sources)

    # Save the combined page sources to a file
    with open(f'all_page_sources_{selected_market}_{selected_msrating}_rows{pagerows}_{timestamp}.html', 'w', encoding='utf-8') as file:
        file.write(combined_page_sources)
    ###########################filter result table##################################
    ###########filter results to more than 20% return###############################
    # Filter rows with 'FP_ratio_percent' greater than 20
    percent_threshold = 15
    filtered_rows = [info_list for info_list in all_info_lists if float(info_list[3]) > percent_threshold]

    # Save filtered rows to a new CSV file
    filtered_csv_file_path = f'filtered_info_lists_thr{percent_threshold}_{selected_market}_{selected_msrating}_rows{pagerows}_{timestamp}.csv'

    with open(filtered_csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header (if applicable)
        csv_writer.writerow(['Fair_value_estimate', 'Price', 'FP_ratio', 'FP_ratio_percent', 'Uncertainty', 'cost_allocation', 'Economic_moat', 'Security_Name', 'Security_Symbol'])

        # Write each filtered row to the CSV file
        csv_writer.writerows(filtered_rows)

    print(f"Filtered info lists (FP_ratio_percent > {percent_threshold}) saved to: {filtered_csv_file_path}")
    data = pd.read_csv(filtered_csv_file_path)
    print(data)
    '''
    #save  page_sources to a new csv file
    filtered_csv_file_path = f'pa_thr{percent_threshold}_{selected_market}_{selected_msrating}_rows{pagerows}_{timestamp}.csv'

    with open(filtered_csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
    '''

    ################################################################################
    try:
        #wait = WebDriverWait(driver, wait_val)
        # Get the page source after logging in
        current_url = driver.current_url
        driver.get(current_url)
        html_content = driver.page_source

        print(current_url)
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        input("Press Enter to close the browser window.")
        driver.quit()

def on_run_button_click():
    # Get the input values from the entry widgets
    input1_value = entry1.get()
    input2_value = entry2.get()
    input3_value = entry3.get()
    input4_value = entry4.get()
    input5_value = entry5.get()
    input6_value = entry6.get()



    # Check if both inputs are provided
    if input1_value and input2_value and input3_value and input4_value and input5_value and input6_value:
        run_program(input1_value,input2_value,input3_value,input4_value,input5_value,input6_value)
        app.destroy()
    else:
        messagebox.showerror("Error", "Please provide values for All inputs.")

# Create the main application window
app = tk.Tk()
app.title("Python Program Runner")

# Create and place input widgets
label1 = ttk.Label(app, text="User ID:")
label1.grid(row=0, column=0, padx=10, pady=5, sticky="E")
entry1 = ttk.Entry(app)
entry1.grid(row=0, column=1, padx=10, pady=5)

label2 = ttk.Label(app, text="Password:")
label2.grid(row=1, column=0, padx=10, pady=5, sticky="E")
entry2 = ttk.Entry(app)
entry2.grid(row=1, column=1, padx=10, pady=5)

label3 = ttk.Label(app, text="Market(NASDAQ or NYSE or LSE):")
label3.grid(row=2, column=0, padx=10, pady=5, sticky="E")
entry3 = ttk.Entry(app)
entry3.grid(row=2, column=1, padx=10, pady=5)

label4 = ttk.Label(app, text="Star No.(stars_all or stars_5 or stars_4 or stars_3):")
label4.grid(row=3, column=0, padx=10, pady=5, sticky="E")
entry4 = ttk.Entry(app)
entry4.grid(row=3, column=1, padx=10, pady=5)

label5 = ttk.Label(app, text="load time(s):")
label5.grid(row=4, column=0, padx=10, pady=5, sticky="E")
entry5 = ttk.Entry(app)
entry5.grid(row=4, column=1, padx=10, pady=5)

label6 = ttk.Label(app, text="Web Driver Wait(s):")
label6.grid(row=5, column=0, padx=10, pady=5, sticky="E")
entry6 = ttk.Entry(app)
entry6.grid(row=5, column=1, padx=10, pady=5)


# Create and place the "Run" button
run_button = ttk.Button(app, text="Run Program", command=on_run_button_click)
run_button.grid(row=6, column=0, columnspan=2, pady=10)

# Start the GUI event loop
app.mainloop()
