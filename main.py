from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import base64
import time
import pdfkit
import os.path
import multiprocessing as mp
import re

options = Options()

# set window size to native GUI size
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(
    "https://lookerstudio.google.com/reporting/82873787-8a91-467a-9272-403bf662d37b/page/t3poC")

time.sleep(5)

with open("data.png", "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())

#  Style the image added to the page
driver.execute_script(
    "const para = document.createElement('img'); para.src='data:image/png;base64," + converted_string.decode() + "'; para.style.position='absolute'; para.style.top= '0.6%'; para.style.left='1.2%'; para.style.width='756px'; para.style.height='2610px'; para.alt='data.png'; const parent = document.querySelector('.ng2-canvas-container'); parent.appendChild(para);")

# Remove <script> in <script
real_page_source = ''
tmp = driver.page_source.replace('<script>', '')

# Remove all scripts
first_filter_list = tmp.split('<script')
for element in first_filter_list:
    if ("script>" not in element):
        real_page_source = real_page_source + element
    else:
        useful_position = element.find('script>')+7
        real_page_source = real_page_source + element[useful_position:]

# Remove unncessary stylesheet
real_page_source = real_page_source.replace(
    '<link rel="stylesheet" type="text/css" href="https://ssl.gstatic.com/datastudio/20230131_00020038/css/material_theme.css?cb=505891980" nonce="">', "")
real_page_source = real_page_source.replace(
    '<link rel="stylesheet" type="text/css" href="https://ssl.gstatic.com/datastudio/20230131_00020038/css/css.css?cb=505891980" nonce="">', "")

# Remove unnecessary code
real_page_source = real_page_source.replace('<base href="/">', '')
second_filter_start = real_page_source.find('!function')
second_fitler_end = real_page_source.find('var ke=') + 8
real_page_source = real_page_source[:second_filter_start] + \
    real_page_source[second_fitler_end:]

# Update Image Url
real_page_source = real_page_source.replace(
    'src="//www.gstatic.com/analytics-lego', 'src="https://www.gstatic.com/analytics-lego/svg/ic_looker_studio.svg"')
real_page_source = real_page_source.replace(
    'src="//www.gstatic.com/analytics-suite/header/suite', 'src="https://www.gstatic.com/analytics-suite/header/suite/v2/ic_account_circle_dark.svg"')

# import css
with open('style.css', 'r') as file:
    style = file.read()

real_page_source = real_page_source.replace(
    '<head>', '<head><style type="text/css">' + style + '</style>')

# output HTML
with open("Output//data.html", "w", encoding="utf-8") as my_file:
    my_file.write(real_page_source)

# Output PDF
time.sleep(5)

options = {
    "encoding": "UTF-8",  # Set the encoding format, here utf8 is an example, which encoding to use depends on what your html file uses
    'javascript-delay': '2000',  # Set waiting time for javascript rendering
    # The following is to set the style of the picture
    "custom-header": [('Accept-Encoding', 'gzip')],
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'page-height': '1333',
    'page-width': '800',
    'no-outline': False,
}

path_wkhtmltopdf = r'.\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
pdfkit.from_url("Output/data.html",
                "Output//data.pdf", verbose=True, configuration=config)
