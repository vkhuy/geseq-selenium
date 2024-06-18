import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoAlertPresentException
import time
import os
import os.path
import sys

import logging
from logging import Formatter
from logging import FileHandler

#Set up log file

logger = logging.getLogger('mylog')
logger.setLevel(logging.DEBUG)
formatter = Formatter('%(asctime)s - %(levelname)s - [in %(pathname)s:%(lineno)d] - %(message)s')

# Specify the directory where you want to save the log file
log_directory = os.getcwd()  # This will get the current working directory
log_file_name = 'geseq.log'  # Log file name
log_file_path = os.path.join(log_directory, log_file_name)  # Combining directory and filename_file_path = FileHandler(os.path.join(log_directory, 'geseq.log')) 

# Ensure the log directory exists
os.makedirs(log_directory, exist_ok=True)

# Configure FileHandler to overwrite the log file
file_handler = FileHandler(log_file_path, mode='a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Set up command-line argument for the file path
parser = argparse.ArgumentParser(description='An selenium script to upload a FASTA file to GESEQ')
parser.add_argument('file_path', type=str, help='Path to the FASTA file')
args = parser.parse_args()
args.file_path = os.path.abspath(args.file_path.strip())  # Convert to absolute path

# Set up firefox profile

options = Options()

options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", os.getcwd() )
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

# Get driver
logger.info('******************** START ********************')

driver = webdriver.Firefox(options=options)

driver.get("https://chlorobox.mpimp-golm.mpg.de/geseq.html#")
time.sleep(15)

logger.info('Get into GESEQ web')


upload_file = driver.find_element(by=By.CSS_SELECTOR, value="#gs_application > div > div:nth-child(1) > div:nth-child(1) > div.gs_panelcontent > div.filelist > div.fl_head > input[type=file]")
upload_file.send_keys(args.file_path)

logger.info('Upload FASTA file')
time.sleep(5)
shape = driver.find_element(by=By.CSS_SELECTOR, value="#ogd_shape_circular") 
shape.click()

source = driver.find_element(by=By.CSS_SELECTOR, value="#gssrctype_chloro")
source.click()

disclaimer = driver.find_element(by=By.CSS_SELECTOR, value="#cb_disclaimer")
disclaimer.click()

rnascan = driver.find_element(by=By.CSS_SELECTOR, value="#trnascanv2_enabled")
rnascan.click()

logger.info('Click parameter')

time.sleep(5)
submit = driver.find_element(by=By.CSS_SELECTOR, value= "#gs_application > div > div.x4_column.x4_column_last > div.gs_panel.gs_actions > div.gs_panelcontent > div > a.gs_submit.cms_button")
submit.click()

title = driver.find_element(by=By.CSS_SELECTOR, value= "#submit_dialog > div.x4_taxoinnerdialog > div > div > div.x4_value > input")
title.clear()

time.sleep(5)
submit_ok = driver.find_element(by=By.CSS_SELECTOR, value= ".cms_button_ok")
submit_ok.click()
logger.info('Submit')

time.sleep(300)
save_button = driver.find_element(by=By.CSS_SELECTOR, value= "#gs_application > div > div.x4_column.x4_column_last > div:nth-child(3) > div.gs_panelhead > a")
save_button.click()

time.sleep(60)
download = driver.find_element(by=By.CSS_SELECTOR, value= "#io_dialog_tail > span > a.cms_button.cms_button_ok")
download.click()
logger.info('Download result')

time.sleep(200)
try:
    logger.info('Before quitting Firefox')

    # Dismiss any open alerts
    try:
        driver.switch_to.alert.dismiss()
        logger.info('Dismissed open alert')
    except NoAlertPresentException:
        logger.info('No open alert to dismiss')

    # Set timeouts
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)

    driver.quit()
    logger.info('After quitting Firefox')
except Exception as e:
    logger.error(f'Error while quitting Firefox: {e}')



# path = "./" + "Geseq - " + "ON381735_1.fasta"

# check_file = os.path.exists(path)

# if check_file == True:
#     print("Annotation was successful")
# else:
#     print("Annotation was not successful")

# example = driver.find_element(by=By.CSS_SELECTOR, value="#gs_application > div > div.x4_column.x4_column_last > div.gs_panel.gs_actions > div.gs_panelcontent > div > a:nth-child(3)")
# example.click()


logger.info('********************* END *********************')

sys.exit(0)
