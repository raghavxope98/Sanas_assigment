# Sanas_assigment
Objective
The goal of this script is to automate the following tasks:
1. Launch the browser.
2. Open URL - http://www.google.com
3. Enter the keyword "amazon" in the search bar
4. print all the search results
5. Click on the link which takes you to the amazon login page.
6. login to https://www.amazon.in/
7. click on all buttons on search & select Electronics.
8. search for dell computers
9. apply the filter of range Rs 30000 to 50000
10. Validate all the products on the first 2 pages are shown in the range of Rs 30000 to 50000
11. print all the products on the first 2 pages whose rating is 5 out of 5


Tried the below steps but could not perform it since to add it wish list the user should be logged in and to login we will encounter to read from captcha so could not find the right approch.  
12. add the first product whose rating is 5 out of 5 to the wish list. (Create a new wish list)
13. Validate the product is added to the wish list

Instead of the above steps I have tried to add the Items to cart and verify
12. add the first product whose rating is 5 out of 5 to the cart. (Create a new wish list)
13. Validate the product is added to the cart

Prerequisites:
Ensure you have the following installed:
Python 3.x
Selenium WebDriver
Chrome WebDriver 
Usage
Run the script: python amazon_automation.py.

Configuration
Before running the script, make sure to update the following variables in the script:
WEB_DRIVER_PATH: Path to the WebDriver executable.
PRICE_RANGE_MIN: Minimum price range filter.
PRICE_RANGE_MAX: Maximum price range filter.

Notes
Ensure you have a stable internet connection for seamless execution.
The script might require adjustments based on any changes in the Amazon website layout or functionality.
Feel free to contribute to the script by enhancing its functionality or improving its efficiency.
