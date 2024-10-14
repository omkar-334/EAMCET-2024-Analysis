import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from driver import create_driver

driver, wait = create_driver()

dropdown1 = wait.until(
    EC.visibility_of_element_located((By.ID, "MainContent_DropDownList1"))
)
select1 = Select(dropdown1)
colleges = [element.get_attribute("value") for element in select1.options]

cdict = {}

for college in colleges:
    dropdown1 = wait.until(
        EC.visibility_of_element_located((By.ID, "MainContent_DropDownList1"))
    )
    select1 = Select(dropdown1)
    select1.select_by_value(college)
    print(college, end=" --- ")

    dropdown2 = wait.until(
        EC.visibility_of_element_located((By.ID, "MainContent_DropDownList2"))
    )
    select2 = Select(dropdown2)
    branches = [branch.get_attribute("value") for branch in select2.options]
    branches = [i for i in branches if len(i) == 3]

    cdict[college] = branches

    with open("colleges.json", "w") as json_file:
        json.dump(cdict, json_file, indent=4)
