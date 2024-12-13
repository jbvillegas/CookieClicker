from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

#Clicking on the cookie
try:
    cookie = driver.find_element(by=By.ID, value="cookie")
except Exception as e:
    print(f"Error finding cookie element: {e}")
    driver.quit()
    exit()

#Get the id's
try:
    items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
except Exception as e:
    print(f"Error finding store item elements: {e}")
    driver.quit()
    exit()
item_ids = [item.get_attribute("id") for item in items]

#Intervals for purchasing times
INTERVAL = 5
RUN_TIME = 300
timeout = time.time() + INTERVAL
five_min = time.time() + RUN_TIME

#Parse money element.
def parse_money_element(text):
    if "," in text:
        text = text.replace(",", "")
    return int(text)

try:
    while True:
        cookie.click()

        if time.time() >= timeout:
            timeout += INTERVAL

            try:
                all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
            except Exception as e:
                print(f"Error finding store prices: {e}")
                continue

            item_prices = []

            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    cost = int(element_text.split("-")[1].strip().replace(",", ""))
                    item_prices.append(cost)

            cookie_upgrades = {}
            for n in range(len(item_prices)):
                cookie_upgrades[item_prices[n]] = item_ids[n]

            try:
                money_element = driver.find_element(by=By.ID, value="money").text
                cookie_count = parse_money_element(money_element)
            except Exception as e:
                print(f"Error parsing money element: {e}")
                cookie_count = 0
                continue

            affordable_upgrades = {}
            for cost, id in cookie_upgrades.items():
                if cookie_count >= cost:
                    affordable_upgrades[cost] = id

            #Choose expensive instead of affordable
            if affordable_upgrades:
                highest_price_affordable_upgrade = max(affordable_upgrades)
                print(f"Purchasing upgrade with ID {affordable_upgrades[highest_price_affordable_upgrade]} "
                      f"at price {highest_price_affordable_upgrade}")
                to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

                try:
                    driver.find_element(by=By.ID, value=to_purchase_id).click()
                except Exception as e:
                    print(f"Error clicking upgrade {to_purchase_id}: {e}")
            else:
                print("No upgrades are affordable at this time.")

        #Runtime of 5 minutes.
        if time.time() >= five_min:
            try:
                cookie_per_s = driver.find_element(by=By.ID, value="cps").text
                print(f"Cookies per second: {cookie_per_s}")
            except Exception as e:
                print(f"Error retrieving cookies per second: {e}")
            finally:
                break

finally:
    print("Exiting and closing the browser.")
    driver.quit()
