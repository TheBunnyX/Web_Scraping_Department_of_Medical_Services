import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import xlsxwriter
import openpyxl

def total_pages():
    service = Service(executable_path = "chromedriver.exe")
    driver = webdriver.Chrome(service = service)
    driver.get("https://porta.fda.moph.go.th/FDA_SEARCH_ALL/MAIN/SEARCH_CENTER_MAIN.aspx")

    input_element = driver.find_element(By.CLASS_NAME, "input-lg")
    A = "ยาหอมอินทจักร์"
    input_element.send_keys(A + Keys.ENTER)

    checkbox_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_CheckBoxList1_2"))
    )
    checkbox_element.click()
    search = driver.find_element(By.CLASS_NAME, "btn-lg")
    search.click()

    try :
        combobox = driver.find_element(By.NAME ,"ctl00$ContentPlaceHolder1$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox")
        combobox.click()
        combobox.send_keys(Keys.ARROW_DOWN)
        combobox.send_keys(Keys.ARROW_DOWN)
        combobox.send_keys(Keys.ENTER)
        time.sleep(3)
    except :
        time.sleep(3)
        #time.sleep(10)

    # Get the total number of pages
    try:
        total_item_text = driver.find_element(By.XPATH, '/html/body/form/div[3]/div[2]/div/div/div[2]/div[2]/div/center/div/table/tfoot/tr/td/table/tbody/tr/td/div[5]/strong[1]').text
        total_item = int(total_item_text)
    except :
        time.sleep(3)
        print("1 < item")
        total_item = 1
        
    driver.quit()    
    return total_item 
    

def scraping_search(n):
    service = Service(executable_path = "chromedriver.exe")
    driver = webdriver.Chrome(service = service)

    driver.get("https://porta.fda.moph.go.th/FDA_SEARCH_ALL/MAIN/SEARCH_CENTER_MAIN.aspx")

    input_element = driver.find_element(By.CLASS_NAME, "input-lg")
    A = "ยาหอมอินทจักร์"
    input_element.send_keys(A + Keys.ENTER)

    checkbox_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_CheckBoxList1_2"))
    )
    checkbox_element.click()
    search = driver.find_element(By.CLASS_NAME, "btn-lg")
    search.click()

    try :
        combobox = driver.find_element(By.NAME ,"ctl00$ContentPlaceHolder1$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox")
        combobox.click()
        combobox.send_keys(Keys.ARROW_DOWN)
        combobox.send_keys(Keys.ARROW_DOWN)
        combobox.send_keys(Keys.ENTER)
        time.sleep(3)
    except :
        time.sleep(3)
        #time.sleep(10)
        
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
                    #print("found at idx {} = {}".format(index,item))
                    # row[index] = idx16
                    driver.switch_to.new_window()
                    driver.get(idx16)
                    tabs_value = driver.window_handles
                    #print(tabs_value)
                    current_value = driver.current_window_handle
                    #print(current_value)
                    value1 = driver.find_element(By.ID,"ContentPlaceHolder1_lb_sale_channel")   #ช่องทางการขาย
                    val1txt = value1.text
                    value2 = driver.find_element(By.ID,"ContentPlaceHolder1_lb_indication")   #ข้อบ่งใช้
                    val2txt = value2.text
                    value3 = driver.find_element(By.ID,"ContentPlaceHolder1_lb_thanm")     #ชื่อบริษัท
                    val3txt = value3.text
                    #print("value1 = {} value2 = {} value2 = {} ".format(val1txt,val2txt,val3txt))
                    row[index] = val1txt
                    row.append(val2txt)
                    row.append(val3txt)
                    #print(row)
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
            time.sleep(3)  # Allow time for the next page to load

    # Create the Excel file
    df = pd.DataFrame(data)
    #writer = pd.ExcelWriter('testdelrow.xlsx', engine='xlsxwriter')
    #df.to_excel(writer, sheet_name='welcome', index=False)
    #writer.close()

    #drop column

    #df = pd.read_excel("testdelrow.xlsx")
    test = 0
    for round_num in range(total_pages): 
        if(round_num == 0):
            start_row = round_num*(50 + test)
            end_row = start_row + 36
            df = df.drop(df.index[start_row:end_row])
            test + 1
        else:
            start_row = round_num*(50 + test)
            end_row = start_row + 38
            df = df.drop(df.index[start_row:end_row])
            test + 1
            
    # Save the modified workbook
    
    df.to_excel("testdelrow.xlsx", index = False)

    #df = pd.read_excel("testdelrow.xlsx")

    df[5] = df[5].apply(str)

    #for round_num in range(1): 
    df = df.drop(df.columns[[0,2,3,6,7,9,11,12,13,15]],axis = 1) # , 6
    
    Data1 = df
    
    driver.quit()  
    #df.to_excel("test"+'.xlsx', index = False)
    return Data1


if __name__ == "__main__":
    
    pool = multiprocessing.Pool(processes = 10)  # Create a pool of 2 processes
    count_item = 129#total_pages()
    
    #service = Service(executable_path = "chromedriver.exe")
    #driver = webdriver.Chrome(service = service)
    #Data_center = first_search()
    count = 0
    #while(len(Data_center)<=count_item):
    Data_center = []
    print("count",len(Data_center))
    Data1 = []
    Data2 = []
    
    results = []
    # Apply the square and cube functions to each number
    for n in range(10):
        result = pool.apply_async(scraping_search, (n,))
        results.append(result)

    result = [res.get() for res in results]
    result1 = result[0]
    result2 = result[1]
    result3 = result[2]
    result4 = result[3]
    result5 = result[4]
    result6 = result[5]
    result7 = result[6]
    result8 = result[7]
    result9 = result[8]
    result10 = result[9]

    pool.close()
    pool.join()
    
    df1 = pd.DataFrame(result1)
    df2 = pd.DataFrame(result2)
    df3 = pd.DataFrame(result3)
    df4 = pd.DataFrame(result4)
    df5 = pd.DataFrame(result5)
    df6 = pd.DataFrame(result6)
    df7 = pd.DataFrame(result7)
    df8 = pd.DataFrame(result8)
    df9 = pd.DataFrame(result9)
    df10 = pd.DataFrame(result10)
    
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7 ,df8 ,df9 ,df10], ignore_index = True) #รวม    
    
    df.to_excel("test565"+'.xlsx', index = False)
    
    df5 = df.drop_duplicates(subset = [4])  #correct
    
    df5.to_excel("test"+'.xlsx', index = False)
    #Remove duplicates from results and results1
    if not Data_center:
        #put in data
        print("Data_center is empty")
        
    else:
        #check duplicate 
        print("Data_center is not empty")   
        
    
    # Apply the square and cube functions to each number
    """    
    for n in numbers:
        
        result_cube = pool.apply_async(cube, (n,))
        
        results1.append((result_square.get()))

    pool.close()
    pool.join()

    """
    # Remove duplicates from results and results1
    #numbers = list(set(numbers + results))

    print("total pages = ", count_item)
    #print(numbers)








