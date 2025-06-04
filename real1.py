from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import xlsxwriter

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
file = open("informationt.txt","w")

driver.get("https://porta.fda.moph.go.th/FDA_SEARCH_ALL/MAIN/SEARCH_CENTER_MAIN.aspx")

input_element = driver.find_element(By.CLASS_NAME, "input-lg")
input_element.send_keys("ขมิ้นชัน" + Keys.ENTER)

# Locate the checkbox and click it
checkbox_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_CheckBoxList1_2"))
)
checkbox_element.click()

# Proceed with the rest of the search logic 
search = driver.find_element(By.CLASS_NAME, "btn-lg")
search.click()

time.sleep(5)  

tbody = driver.find_element(By.XPATH,'/html/body/form/div[3]/div[2]/div/div/div[2]/div[2]/div/center/div/table/tbody')

data = []

for tr in tbody.find_elements(By.XPATH,'//tr'):
    row = [item.text for item in tr.find_elements(By.XPATH,'.//td')]
    data.append(row)
print(len(data))
df = pd.DataFrame(data)
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.close()

#driver.quit()