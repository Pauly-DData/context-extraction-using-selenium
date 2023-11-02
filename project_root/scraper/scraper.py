from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Setup the browser with headless option
chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)

def get_introduction_text(browser):
    # Find the first two <h2> elements with the 'wp-block-heading' class
    headers = browser.find_elements(By.XPATH, "//h2[contains(@class, 'wp-block-heading')]")
    if len(headers) < 2:
        raise ValueError("Not enough headers found on the page for the specified task.")

    # Extract the text from the first header to the second
    start_point = headers[0]
    end_point = headers[1]
    introduction_text = browser.execute_script("""
        var startElem = arguments[0];
        var endElem = arguments[1];
        var content = [];
        var sibling = startElem.nextSibling;
        
        while(sibling && sibling != endElem) {
            content.push(sibling.innerText || sibling.textContent);
            sibling = sibling.nextElementSibling;
        }
        
        return content.join(' ');
    """, start_point, end_point)
    
    return introduction_text.strip()

def get_codemirror_content(driver):
    # Try to get content using common CodeMirror configurations
    js_script = """
    var editors = document.querySelectorAll('.CodeMirror');
    var content = [];
    editors.forEach(editor => {
        if (editor.CodeMirror) {
            content.push(editor.CodeMirror.getValue());
        }
    });
    return content;
    """
    return driver.execute_script(js_script)

try:
    browser.get('https://thecleverprogrammer.com/2023/08/07/netflix-subscriptions-forecasting-using-python/')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror")))

    # Extract the introduction text
    intro_text = get_introduction_text(browser)
    
    # Extract the code contents
    code_contents = get_codemirror_content(browser)

    # Start writing data to a CSV file
    filename = "code_with_introduction.csv"
    with open(filename, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(["Introduction", "Code", "URL", "Editor Number"])
        
        # Write the introduction text only once
        writer.writerow([intro_text, "", "https://thecleverprogrammer.com/2023/08/07/netflix-subscriptions-forecasting-using-python/", ""])
        
        # Write each code snippet in a new row
        for i, code_content in enumerate(code_contents):
            writer.writerow(["", code_content, "https://thecleverprogrammer.com/2023/08/07/netflix-subscriptions-forecasting-using-python/", i + 1])
    
    print(f"Data saved to {filename}")
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    browser.quit()
