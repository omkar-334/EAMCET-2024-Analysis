import json
from io import StringIO

import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from driver import create_driver, mismatch

driver, wait = create_driver()

with open("colleges.json", "r") as json_file:
    colleges = json.load(json_file)

college_dataframes = {}

new = False

for college, branches in colleges.items():
    print(college, end=" --- ")
    college_df = pd.DataFrame()

    for branch in branches:
        print(branch, end=" - ")

        try:
            if new:
                driver, wait = create_driver()
                new = False

            dropdown1 = wait.until(EC.visibility_of_element_located((By.ID, "MainContent_DropDownList1")))
            select1 = Select(dropdown1)
            select1.select_by_value(college)
            driver.implicitly_wait(2)

            dropdown2 = wait.until(EC.visibility_of_element_located((By.ID, "MainContent_DropDownList2")))
            select2 = Select(dropdown2)
            select2.select_by_value(branch)

            submit = wait.until(EC.element_to_be_clickable((By.ID, "MainContent_btn_allot")))
            submit.click()

            if mismatch(driver):
                new = True
                continue

            table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "sortable")))
            table = table.get_attribute("outerHTML")

            df = pd.read_html(StringIO(table))[0]
            df["Branch"] = branch

            df.to_excel("excel.xlsx", index=False)
            college_df = pd.concat([college_df, df], ignore_index=True)

        except (NoSuchElementException, TimeoutException) as e:
            print(f"{e}, branch skip")
            driver.quit()
            new = True

    college_dataframes[college] = college_df
    print()

with pd.ExcelWriter("colleges.xlsx") as writer:
    for college, df in college_dataframes.items():
        df.to_excel(writer, sheet_name=college, index=False)
