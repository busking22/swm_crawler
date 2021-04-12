import re
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


URL = "https://www.swmaestro.org/sw/main/main.do"

driver = webdriver.Chrome(executable_path="chromedriver")
driver.implicitly_wait(time_to_wait=5)
febx = driver.find_element_by_xpath


def swm_login(e_mail, PW):
    driver.get(url=URL)
    box_main_login = febx('//*[@id="header"]/div[1]/ul/li[1]/button')
    box_main_login.click()

    box_id = febx('//*[@id="username"]')
    box_pw = febx('//*[@id="password"]')
    box_id.send_keys(e_mail)
    box_pw.send_keys(PW)

    box_login = febx('//*[@id="login_form"]/div/div[1]/div/dl/dd/button')
    box_login.click()

    driver.switch_to.alert.accept()


def open_mentee():
    box_main_mypage = febx('//*[@id="header"]/div[1]/ul/li[2]/button')
    box_main_mypage.click()

    box_mentee_mentor = febx('//*[@id="contentsList"]/div/div/ul[1]/li[2]/a')
    box_mentee_mentor.click()

    box_search_mentee = febx('//*[@id="contentsList"]/div[1]/div/div/div[2]/div[1]/div/div/button')
    box_search_mentee.click()


def get_info(start=1, end=180):
    with open("./mentee_infos.csv", "w") as file:
        label_dic = {
            1: "Name",
            3: "Email",
            4: "Major",
            5: "Address",
            7: "Project",
            8: "Introduction",
        }
        for label in label_dic.keys():
            file.write(f"{label}\t")
        file.write("\n")

        for num in range(start, end + 1):
            file.write(f"{num}\t")

            box_target_mentee = febx(f'//*[@id="searchList"]/div/table/tbody/tr[{num}]/td[2]/a')
            box_target_mentee.click()
            driver.switch_to.window(driver.window_handles[2])

            for label in label_dic.keys():
                info = febx(f'//*[@id="listFrm"]/div/ul/li[{label}]/dl/dd').get_attribute(
                    "innerHTML"
                )
                info = re.sub("\n", " ", info)
                file.write(f"{info}\t")

            file.write("\n")
            driver.close()
            driver.switch_to.window(driver.window_handles[1])


def main(login_email, login_pw, start_label, end_label):
    swm_login(login_email, login_pw)
    open_mentee()
    driver.switch_to.window(driver.window_handles[1])
    get_info(start_label, end_label)