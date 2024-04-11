import time
from selenium.common import StaleElementReferenceException, TimeoutException, NoSuchElementException
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
               print("The product {} has rating {}".format(product,rating))
    return result


def wait_for_element_present(locator):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def amazonLogin(driver,email,password):
    email_field = driver.find_element(By.ID, "ap_email")
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)
    password_field = driver.find_element(By.ID, 'ap_password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)


def addingToCart(products,productCount=1):
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


def addingToWishlist(products):
        for product in products.keys():
            productLink = products[product]["product_link"]
            driver.get(productLink)
            driver.find_element(By.LINK_TEXT, "Add to Wish List").click()
            amazonLogin(driver=driver, email=username, password=password)


def verifyCart(products):
    driver.get("https://www.amazon.in/gp/cart/view.html")
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sc-list-item-content")))
    item_titles = driver.find_elements(By.CSS_SELECTOR, '.sc-product-title')
    for title in item_titles:
        print(type(title.text))
        print(title.text)
        if '…' in title.text:
            element = title.text.split('…')[0]
        else:
            element = title.text
        if products.find(element):
            print("added to cart")




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
productCategory = inputData['productFilter']['productCategory']
minPrice = inputData['productFilter']['minPrice']
maxPrice = inputData['productFilter']['maxPrice']
ratings = inputData['productFilter']['ratings']

driver = webdriver.Chrome()
driver.get(searchEngineURL)
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("amazon")
search_box.send_keys(Keys.RETURN)
WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3")))
search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
for result in search_results:
    print(result.text)
amazon_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Amazon")
amazon_link.click()
dropdown = Select(driver.find_element(By.ID, "searchDropdownBox"))
dropdown.select_by_visible_text(productCategory)
search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys(productName)
search_box.send_keys(Keys.RETURN)
price_filter_low = driver.find_element(By.ID, "low-price")
price_filter_low.send_keys(minPrice)
price_filter_high = driver.find_element(By.ID, "high-price")
price_filter_high.send_keys(maxPrice)
driver.find_element(By.XPATH, "//input[@class='a-button-input']").click()
product_elements = driver.find_elements(By.CSS_SELECTOR, "[data-component-type='s-search-result']")
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

print(product_details)
cartItems = getProductDetails(product_details, rating=ratings)
if cartItems is not None:
    addingToCart(cartItems,productCount)
driver.quit()
