import time
from selenium.common import TimeoutException, NoSuchElementException
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import json


def wait_for_product_elements():
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']")))
        return True
    except TimeoutException:
        return False


def getProductDetails(allProducts, rating="4.0"):
    result = {}
    for product in allProducts.keys():
        for key,value in allProducts[product].items():
            if key == 'rating' and value == rating:
               result.update({product: allProducts[product]})
    return result


def wait_for_element_present(locator):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def amazonLogin(driver,email,password):
    driver.find_element(By.ID, "nav-link-accountList-nav-line-1").click()
    email_field = driver.find_element(By.ID, "ap_email")
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)
    password_field = driver.find_element(By.ID, 'ap_password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)


def addingToCart(driver,products,productCount=1):
    for product in products.keys():
        if productCount==0:
            print("Finished adding products to the cart as per user mentioned count")
            break
        productLink = products[product]["product_link"]
        driver.get(productLink)
        print("Adding {} successfully to cart".format(product))
        try:
            driver.find_element(By.XPATH, "//div[@class='a-section a-spacing-none a-padding-none']//input[@id='add-to-cart-button']").click()
            time.sleep(10)
            driver.find_element(By.ID, "attach-close_sideSheet-link")
        except:
            print(" product {} was not able to add to the cart".format(product))
        productCount -=1
    verifyCart(product)


def addingToWishlist(driver,products,productCount=1,wishListName='tet123'):
    for product in products.keys():
        if productCount == 0:
            print("Finished adding products to the wishList as per user mentioned count")
            break
        productLink = products[product]["product_link"]
        driver.get(productLink)
        driver.find_element(By.XPATH, "//input[@id='add-to-wishlist-button']").click()
        linkObj = wait_for_element_present((By.XPATH, "//span[@class='a-size-small atwl-hz-vertical-align-middle']"))
        linkObj.click()
        createList = wait_for_element_present((By.XPATH, "//input[@id='list-name']"))
        createList.clear()
        createList.send_keys(wishListName)
        linkObj = wait_for_element_present((By.XPATH, "/html[1]/body[1]/div[10]/div[1]/div[1]/div[1]/form[1]/div[2]/span[3]/span[1]/span[1]/input[1]"))
        linkObj.click()
        time.sleep(10)
        productCount -= 1
        verifyWishList(product,wishListName)


def verifyWishList(product,wishListName):
    driver.get("https://www.amazon.in/hz/wishlist/ls")
    time.sleep(10)
    xpathWishList = "//span[contains(., '" + wishListName + "')]"
    driver.find_element(By.XPATH, xpathWishList).click()
    item_titles = driver.find_elements(By.XPATH,"//div[@class='a-row a-size-small']/h2/a")
    for title in item_titles:
        if '…' in title.text:
            element = title.text.split('…')[0]
        else:
            element = title.text
        if element in product:
            print("===================================================================")
            print("Product successfully added to Wish list")
            print("===================================================================")
        else :
            print("product {} not found in wish list {}".format(product,wishListName))



def verifyCart(products):
    driver.get("https://www.amazon.in/gp/cart/view.html")
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sc-list-item-content")))
    item_titles = driver.find_elements(By.CSS_SELECTOR, '.sc-product-title')
    for title in item_titles:
        if '…' in title.text:
            element = title.text.split('…')[0]
        else:
            element = title.text
        if products.find(element):
            print("Product successfully added to cart")


def settingPriceFilter(driver,minPrice,maxPrice):
    driver.find_element(By.ID, "p_36-title").click()
    price_filter_low = wait_for_element_present((By.ID, "low-price"))
    price_filter_low.send_keys(minPrice)
    price_filter_high = driver.find_element(By.ID, "high-price")
    price_filter_high.send_keys(maxPrice)
    element = driver.find_element(By.XPATH, "//input[@class='a-button-input']")
    driver.execute_script("arguments[0].click();", element)


def readInputValues(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config


#Reading all values from json file
inputData = readInputValues('config.json')
username = inputData['username']
password = inputData['password']
searchEngineURL = inputData['searchEngineURL']
noPagesToSearch = inputData['noPagesToSearch']
productCount = inputData['productCount']
productName = inputData['productName']
wishListName = inputData['wishListName']
productCategory = inputData['productFilter']['productCategory']
minPrice = inputData['productFilter']['minPrice']
maxPrice = inputData['productFilter']['maxPrice']
ratings = inputData['productFilter']['ratings']


#step 1:Launch the browser.
driver = webdriver.Chrome()

#step 2:Open URL - http://www.google.com
driver.get(searchEngineURL)
search_box = driver.find_element(By.NAME, "q")

#step 3:Enter the keyword "amazon" in the search bar
search_box.send_keys("amazon")
search_box.send_keys(Keys.RETURN)

#step 4.	print all the search results
WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3")))
search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
print("===================================================================")
for result in search_results:
    print(result.text)
print("===================================================================")

#step 5 and 6:Eter the keyword "amazon" in the search bar and Click on the link which takes you to the amazon login page
amazon_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Amazon")
amazon_link.click()
amazonLogin(driver,username,password)

#step 7:Enter the keyword "amazon" in the search bar
dropdown = Select(driver.find_element(By.ID, "searchDropdownBox"))
dropdown.select_by_visible_text(productCategory)

#step 8.	search for dell computers
search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys(productName)
search_box.send_keys(Keys.RETURN)
time.sleep(5)

#step 9.	apply the filter of range Rs 30000 to 50000
settingPriceFilter(driver,minPrice,maxPrice)
product_elements = driver.find_elements(By.CSS_SELECTOR, "[data-component-type='s-search-result']")

#step 10.	Validate all the products on the first 2 pages are shown in the range of Rs 30000 to 50000
product_details = {}
for page in range(noPagesToSearch):
    print("Getting details of page {}".format(page+1))
    for product in product_elements:
        title_element = product.find_element(By.CSS_SELECTOR, ".a-text-normal")
        title = title_element.text
        product_link = title_element.get_attribute("href")
        try:
            rating_element = product.find_element(By.CSS_SELECTOR, ".a-icon-alt")
            rating = rating_element.get_attribute("innerHTML")
            pattern = r'(\d\.\d)'
            match = re.search(pattern, rating)
            rating = match.group(1)
        except NoSuchElementException:
            rating = "Ratings not available"
        try:
            price_element = product.find_element(By.CSS_SELECTOR, ".a-price-whole")
            price = price_element.text
            if not minPrice <= price <= maxPrice:
                print("{}  does not fall under the price range ".format(title))
                continue
        except NoSuchElementException:
            price = "Price not available"
        product_details.update({title: {"price": price, "rating": rating, "product_link": product_link}})
    if page != noPagesToSearch-1:
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        next_button.click()
        if not wait_for_product_elements():
            break
        wait_for_element_present((By.LINK_TEXT, "Next"))
        product_elements = driver.find_elements(By.CSS_SELECTOR, "[data-component-type='s-search-result']")
print("======================================================================")
print("Displaying all the products in page 1 and page 2 after filter is set ")
productName = product_details.keys()
for product in productName:
    print("===================================================================")
    print("Product Name : ",product)
    print("Price : ",product_details[product]['price'])
    print("Rating : ", product_details[product]['rating'])
    print("Product Link : ", product_details[product]['product_link'])
    print("===================================================================")

#step 11.	print all the products on the first 2 pages whose rating is 5 out of 5
cartItems = getProductDetails(product_details, rating=ratings)
print("===================================================================")
print("Below product have rating {}".format(ratings))
productName = cartItems.keys()
for product in productName:
    print("===================================================================")
    print("Product Name : ",product)
    print("Price : ",product_details[product]['price'])
    print("Rating : ", product_details[product]['rating'])
    print("Product Link : ", product_details[product]['product_link'])
    print("===================================================================")

# step 12 and 13.	add the first product whose rating is 5 out of 5 to the wish list. (Create a new wish list) and Validate the product is added to the wish list
if cartItems is not None:
    #addingToCart(driver,cartItems,productCount)
    addingToWishlist(driver, cartItems, productCount, wishListName)

driver.quit()
