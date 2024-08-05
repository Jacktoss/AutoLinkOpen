from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

# Specify the URL here
url_to_open = "https://monke.io/"  # Replace this with the URL you want to open

def setup_driver():
    options = Options()
    options.add_argument('-private')  # Use private browsing
    
    service = Service('C:/path/to/geckodriver.exe')  # Put your path to the geckodriver executable here
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def get_links_safely(driver, context="main"):
    links = []
    try:
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            try:
                href = element.get_attribute('href')
                if href and not href.startswith('javascript:'):
                    links.append(href)
            except StaleElementReferenceException:
                continue
    except Exception as e:
        print(f"Error getting links from {context}: {str(e)}")
    return links

def open_all_links(driver, url):
    driver.get(url)
    print(f"Navigated to: {url}")
    
    # Wait for the page to load
    time.sleep(5)
    
    all_links = set()
    
    # Get links from main page
    main_links = get_links_safely(driver, "main page")
    all_links.update(main_links)
    
    # Get links from iframes
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    for i, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            iframe_links = get_links_safely(driver, f"iframe {i+1}")
            all_links.update(iframe_links)
        except Exception as e:
            print(f"Error switching to iframe {i+1}: {str(e)}")
        finally:
            driver.switch_to.default_content()
    
    print(f"Found {len(all_links)} unique links on the page (including iframes).")
    
    # Open links in new tabs
    for link in all_links:
        try:
            print(f"Opening link: {link}")
            driver.execute_script(f"window.open('{link}', '_blank');")
            time.sleep(0.5)  # Short delay between opening tabs
        except Exception as e:
            print(f"Failed to open link: {link}. Error: {str(e)}")

def main():
    driver = setup_driver()
    try:
        open_all_links(driver, url_to_open)
        input("Press Enter when you're done to close the browser...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
