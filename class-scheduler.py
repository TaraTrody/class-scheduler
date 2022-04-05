from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.action_chains import ActionChains 
import sched,time,datetime, bisect
from datetime import datetime as dt, timedelta
from variables import driver_path, username, password


browser = webdriver.Chrome()
browser.get(('https://t.mmears.com/v2/home'))

# Log in to account
browser.find_element(By.CLASS_NAME, 'sign--26Rs4').click()
username_field = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Email Address']").send_keys(username)
password_field = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Password']").send_keys(password)
sign_in_submit = browser.find_element(By.CLASS_NAME,'button--3uR3-').click()


# Remove Modal
try: 
    time.sleep(8) # is there more efficient way do I need the EC should I use implicit wait?
    element_present = EC.visibility_of_element_located((By.XPATH, '//body/div/div/div/div[3]/div/div[2]')) 
    WebDriverWait(browser, 10).until(element_present)
    pop_up = browser.find_element(By.XPATH, '//body/div/div/div/div[3]/div/div[2]')
    ActionChains(browser).move_to_element_with_offset(pop_up, -20, 0).click().perform()
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div').click()
# Check day
    time.sleep(4)   
   
    def get_next_class():
        class_times = ['06:30', '07:00', '07:30', '08:00', '08:30', '09:00']
        def convert_dates(class_time):
             return dt.strptime(class_time, '%H:%M').time()
        result  = map(convert_dates, class_times)
        current_time = dt.now().time()
        next_class = bisect.bisect_left(list(result),  current_time)
        return class_times[next_class] + " am"

    current_day = dt.now()
    delta = timedelta(hours=24)
    schedule_day = (current_day + delta).strftime('%A')
    next_class = get_next_class()
    
   
    current_day = current_day.strftime('%w') 

    if current_day == '5' or current_day == '6' or current_day == '0': 
        browser.find_element(By.XPATH, '//*[local-name()="svg" and @data-icon="right"]').click()
        schedule_day = 'Monday'

    xpath_str = "//p[normalize-space()='{}']/parent::node()/following-sibling::div//p[text()='{}']".format(schedule_day, next_class)
    class_times = browser.find_element(By.XPATH, xpath_str)  
    print(class_times)

    # for i in class_times:
    #     WebDriverWait(browser,10).until(EC.element_to_be_clickable(i)).click()
    #     browser.find_element(By.XPATH, '//div[normalize-space()="Confirm"]').click()
    #     WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[normalize-space()="No, thanks!"]'))).click()
    #     time.sleep(4)

        
# create loop with schedule function
    
    # get a list of all the time elements under the title
    # for each time 
        # if the text isn't booked or standby booked 
            #refresh page and click element
            #click footer
            #click dialog
            # pause until some time (maybe reset current time and add 30
            # )
    # times_list = ['06:30', '07:00', '07:30', '08:00', '08:30']
    
except Exception as exc:
    print(exc)

# get current day 
# search for current day on page that matches current day
# 6:30 7:00 7:30 8:00 8:30
# time how long it takes for refresh of page and then subtract that time from 630  possibly test this in browser
# if it's not book then schedule 
    # refresh the page seconds before and click at 
    #can you check if the EC can locate based on inner text?
