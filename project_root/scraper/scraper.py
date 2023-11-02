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

try:
    browser.get('https://thecleverprogrammer.com/2023/08/07/netflix-subscriptions-forecasting-using-python/')
    # Wait for the CodeMirror element to be present
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror"))
    )

    # Extract the content from the CodeMirror editor
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

    # Get the code contents
    contents = get_codemirror_content(browser)

    # Create a list to store the structured data
    data = [["Type", "Content", "Code", "Editor Number"]]
    
    for i, content in enumerate(contents):
        data.append([
            "human-code",
            "https://thecleverprogrammer.com/2023/08/07/netflix-subscriptions-forecasting-using-python/",
            content,
            i + 1
        ])

    # Save the data to a CSV file
    filename = "code_data.csv"
    with open(filename, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write a header row
        writer.writerows(data)
    
    print(f"Data saved to {filename}")
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    browser.quit()
