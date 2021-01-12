from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get("https://www.piano-e-competition.com/midi_2018.asp")
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    titre = elem.get_attribute("href")
    if titre.endswith(".MID") or titre.endswith(".mid"):
        try:
            driver.execute_script('''window.open("'''+titre+'''","_blank");''')
        except:
            pass


assert "No results found." not in driver.page_source
driver.close()
