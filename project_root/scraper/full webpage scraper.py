from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # to run browser in the background
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL you want to scrape
url = 'https://thecleverprogrammer.com/2023/08/07/netflix-subscriptions-forecasting-using-python/'

# Navigate to the URL
driver.get(url)

# Use JavaScript to get the text of the entire body
all_content_text = driver.execute_script("return document.body.innerText")

# Output the text
print(all_content_text)

# Close the WebDriver
driver.quit()
