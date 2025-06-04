import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import xlsxwriter

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://porta.fda.moph.go.th/FDA_SEARCH_ALL/MAIN/SEARCH_CENTER_MAIN.aspx")

input_element = driver.find_element(By.CLASS_NAME, "input-lg")
input_element.send_keys("ยาหอมอินทจักร์" + Keys.ENTER)

checkbox_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_CheckBoxList1_2"))
)
checkbox_element.click()
search = driver.find_element(By.CLASS_NAME, "btn-lg")
search.click()

time.sleep(5)

# Get the total number of pages
try:
    total_pages_text = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div/div/div[2]/div[2]/div/center/div/table/tfoot/tr/td/table/tbody/tr/td/div[5]/strong[2]').text
    total_pages = int(total_pages_text)
except NoSuchElementException:
    print("1 page")
    total_pages = 1

data = []
for page_num in range(1, total_pages + 1): 
    tbody = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div/div/div[2]/div[2]/div/center/div/table/tbody')
    for tr in tbody.find_elements(By.XPATH, '//tr'): 
        row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
        try:
            idx16 = tr.find_element(By.LINK_TEXT,value = 'ดูข้อมูล').get_attribute("href")
        except NoSuchElementException:
            print("not found link")
        for index,item in enumerate(row):
            if row[index] == "ดูข้อมูล":
                print("found at idx {} = {}".format(index,item))
                # row[index] = idx16
                driver.switch_to.new_window()
                driver.get(idx16)
                tabs_value = driver.window_handles
                print(tabs_value)
                current_value = driver.current_window_handle
                print(current_value)
                value1 = driver.find_element(By.ID,"ContentPlaceHolder1_lb_sale_channel")
                val1txt = value1.text
                value2 = driver.find_element(By.ID,"ContentPlaceHolder1_lb_indication")
                val2txt = value2.text
                print("value1 = {} value2 = {} ".format(val1txt,val2txt))
                row[index] = val1txt
                row.append(val2txt)
                print(row)
                time.sleep(2)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        #if look last colomn
        #last = [item.text for item in tr.find_elements(By.XPATH, './/td')]
        data.append(row)
    # print(data)        

    # If not the last page, click next
    if page_num < total_pages:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/div[2]/div/div/div[2]/div[2]/div/center/div/table/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]")))
        next_button.click()
        time.sleep(2)  # Allow time for the next page to load

# Create the Excel file
df = pd.DataFrame(data)
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.close()

df = pd.read_excel("test.xlsx")

test = 0
for round_num in range(1): 
    if(round_num == 0):
        start_row = round_num*(50 + test)
        end_row = start_row + 36
        df = df.drop(df.index[start_row:end_row])
        test+1
    else:
        start_row = round_num*(10 + test)
        end_row = start_row + 38
        df = df.drop(df.index[start_row:end_row])
        test + 1

for round_num in range(1): 
    df = df.drop(df.columns[[0,2, 3, 6,7,9,11,12,13,15]],axis = 1)

df.to_excel('test456.xlsx', index = False)

driver.quit()