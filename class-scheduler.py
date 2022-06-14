from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR

import time, bisect
from datetime import datetime as dt, timedelta
from dotenv import load_dotenv
import os 

load_dotenv()
driver_path =  os.getenv("DRIVER_PATH")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

def signIn():
    browser.find_element(By.CLASS_NAME, "sign--26Rs4").click()
    browser.find_element(
        By.CSS_SELECTOR, "input[placeholder='Email Address']"
    ).send_keys(username)
    browser.find_element(By.CSS_SELECTOR, "input[placeholder='Password']").send_keys(
        password
    )
    browser.find_element(By.CLASS_NAME, "button--3uR3-").click()


def removeModal():
    pop_up = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//body/div/div/div/div[3]/div/div[2]")
        )
    )
    ActionChains(browser).move_to_element_with_offset(pop_up, -20, 0).click().perform()
    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div").click()


def get_next_class():
    class_times = ["06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00"]

    def convert_dates(class_time):
        return dt.strptime(class_time, "%H:%M").time()

    result = map(convert_dates, class_times)
    current_time = dt.now().time()
    next_class = bisect.bisect_left(list(result), current_time)

    return class_times[next_class] + " am"


def schedule_class(next_class_time):

    try:
        today = dt.now()
        delta = timedelta(hours=24)  # classes scheduled 24hrs in advance
        schedule_day = (today + delta).strftime("%A")
        next_class = next_class_time

        current_day = today.strftime("%w")

        # Clicks to next page to schedule the Monday class
        if current_day == "0":
            browser.find_element(
                By.XPATH, '//*[local-name()="svg" and @data-icon="right"]'
            ).click()
            schedule_day = "Monday"

        if current_day !="0":     
            browser.refresh()
        else:
            time.sleep(2)

        
        xpath_str = "//p[normalize-space()='{}']/parent::node()/following-sibling::div//p[text()='{}']".format(
            schedule_day, next_class
        )
        class_times = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_str))
        ) # The next line duplicates this

        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(class_times)).click()
        browser.find_element(By.XPATH, '//div[normalize-space()="Confirm"]').click()
        time.sleep(6)
       
    
        WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, ' //div[contains(text(),"OK")]'))
        ).click()

        time.sleep(3)

        confirm_xpath_str = "//p[contains(text(),'{}')]/parent::node()/following-sibling::div//p[text()='{}']//following-sibling::p/text()".format(schedule_day, next_class) 
        confirm_class = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, confirm_xpath_str)))
        print(confirm_class)

    except Exception as exc:
        raise exc

    print("Great! you're schedule for the class")

def listener(event):
    print(f'Job {event.job_id} raised {event.exception.__class__.__name__}')

if __name__ == "__main__":    
    sched = BackgroundScheduler()
    browser = webdriver.Chrome(driver_path)# update package
    browser.get(("https://t.mmears.com/v2/home"))

    signIn()
    time.sleep(5)
    removeModal()
    next_class = get_next_class()

    # next_class = "06:00 am"

    current_date = dt.now().date().strftime("%Y-%m-%d") 
    date_str = f"{current_date} {next_class[:5]}:00"
    # date_str = "2022-06-14 10:09:30"
    
    sched.add_listener(listener, EVENT_JOB_ERROR)
    sched.add_job(schedule_class, "date", run_date=date_str, args=[next_class])


    sched.start()


try:

    for i in range(1, 90):
        time.sleep(2)
    sched.shutdown()
    # browser.quit()
except (KeyboardInterrupt, SystemExit):
    sched.shutdown()