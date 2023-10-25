from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import PyPDF2
# Set Chrome options
service = Service(executable_path='chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--kiosk-printing")

# Initialize the WebDriver with ChromeDriverManager
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("C:\\Users\\Think\\Desktop\\s3_query\\my_html_file.html")  # Replace with your HTML file's URL

# Wait for the page to load (you might need to adjust the waiting time)
driver.implicitly_wait(10)

# Set page size to "legal" and layout to "portrait"
driver.execute_script('''
    var style = document.createElement('style');
    style.innerHTML = 'body { size: legal; margin: 0; padding: 0; }';
    document.head.appendChild(style);
''')

# Print to PDF
pdf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.pdf")

# Print to PDF with the specified file path
driver.execute_script(f'window.print("{pdf_file_path}");')

# Wait for the PDF generation (you might need to adjust the waiting time)
driver.implicitly_wait(10)

# Close the browser
driver.quit()

# View the PDF using PyPDF2
with open(pdf_file_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    pdf_page = pdf_reader.getPage(0)  # Change the page number as needed
    pdf_text = pdf_page.extractText()

print(pdf_text)
