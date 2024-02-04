# import requests
# from bs4 import BeautifulSoup

# def scrape_website(url, output_file_path):
#     # Send an HTTP request to the website
#     response = requests.get(url,allow_redirects=True)
#     #print(response.status_code)
#     print("Final Destination URL:", response.url)
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # Find and extract all text content
#         text_content = soup.get_text(separator='\n')  # Use newline as the separator

#         # Remove extra newline characters
#         text_content = '\n'.join(line.strip() for line in text_content.splitlines() if line.strip())
#         #print(text_content)
#         # Write the scraped text to the output file
#         with open(output_file_path, 'w', encoding='utf-8') as file:
#             file.write(text_content)
        
#         # Return the path of the output file
#         return output_file_path
#     else:
#         print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
#         return None


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrape_website(url, output_file_path):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening the browser window)
        
        # Initialize the Selenium WebDriver with Chrome options
        driver = webdriver.Chrome(options=chrome_options)
        
        # Load the webpage
        driver.get(url)
        
        # Wait for the page to fully load (adjust the sleep duration as needed)
        time.sleep(5)
        
        # Get the HTML content of the page
        html_content = driver.page_source
        
        # Write the HTML content to the output file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print("Scraped content written to", output_file_path)
        
        # Close the WebDriver
        driver.quit()
        
    except Exception as e:
        print("An error occurred:", str(e))
        return False
    return True

# Example usage
#scrape_website("https://www.anastasiabeverlyhills.com/75102191907/checkouts/be6b627b90138f3bd0252c3cfaecea64?no_cookies_from_redirect=1", "scraped_content.txt")
