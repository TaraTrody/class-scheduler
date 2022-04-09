from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 

from apscheduler.schedulers.blocking import BlockingScheduler
import time,datetime, bisect
from datetime import datetime as dt, timedelta
from variables import username, password # NOTE 1: Can this come from the system environ variables?


browser = webdriver.Chrome()
browser.get(('https://t.mmears.com/v2/home'))
sched = BlockingScheduler()

try: 
    # Log in to account
    browser.find_element(By.CLASS_NAME, 'sign--26Rs4').click()
    browser.find_element(By.CSS_SELECTOR, "input[placeholder='Email Address']").send_keys(username)
    browser.find_element(By.CSS_SELECTOR, "input[placeholder='Password']").send_keys(password)
    browser.find_element(By.CLASS_NAME,'button--3uR3-').click()

    
    time.sleep(5) 
    # Removes the modal
    pop_up =  WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH,'//body/div/div/div/div[3]/div/div[2]')))
    ActionChains(browser).move_to_element_with_offset(pop_up, -20, 0).click().perform()
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div').click()

   
    def schedule_class(): 
        # This function defines the job the will select and schedule the upcoming class
        browser.refresh()
            
        def get_next_class():
            # returns the next class time to be scheduled
            class_times = ['06:30', '07:00', '07:30', '08:00', '08:30', '09:00']

            def convert_dates(class_time):
                return dt.strptime(class_time, '%H:%M').time()

            result  = map(convert_dates, class_times)
            current_time = dt.now().time()
            next_class = bisect.bisect_left(list(result),  current_time)

            return class_times[next_class] + " am"
        

        today = dt.now()
        delta = timedelta(hours=24) # classes scheduled 24hrs in advance
        schedule_day = (today + delta).strftime('%A')
        next_class = get_next_class()
        

        current_day = today.strftime('%w') 

        # Clicks to next page to schedule the Monday class 
        if current_day == '5' or current_day == '6' or current_day == '0': 
            browser.find_element(By.XPATH, '//*[local-name()="svg" and @data-icon="right"]').click()
            schedule_day = 'Monday'
            
        # Gets the class element
        xpath_str = "//p[normalize-space()='{}']/parent::node()/following-sibling::div//p[text()='{}']".format(schedule_day, next_class)
        class_times = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath_str)))
        
        # TODO 1: update with logic to check if the sibling of the class time is Not "Booked" continue to schedule class
        xpath_status = "//p[normalize-space()='{}']/parent::node()/following-sibling::div//p[text()='{}']/following-sibling::p".format(schedule_day, next_class)
        status = WebDriverWait(browser, 10).until(EC.presence_of_element_located(By.XPATH, xpath_status ))
        
        if  status.text != 'Booked':
            # Clicks the class time, confirmation button and closes the pop up
            WebDriverWait(browser, 10). until(EC.element_to_be_clickable(class_times)).click()
            browser.find_element(By.XPATH, '//div[normalize-space()="Confirm"]').click()
            # TODO 2: Get the correct element that pops up after scheduling a standby class
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[normalize-space()="No, thanks!"]'))).click()
            
            print("Great! you're schedule for the class")

    # TODO 3: update with correct interval, start and end times
    current_date = dt.now().date() 
    start = f"{current_date} 00:19:00"
    end = f"{current_date} 00:22:00"    
    # FIXME 1: scheduler not ending after endtime
    sched.add_job(schedule_class, 'interval', minutes=1, start_date=start, end_date=end)    
    sched.start()

except Exception as exc:
    print(exc)

browser.quit()