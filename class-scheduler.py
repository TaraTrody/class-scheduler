from selenium import webdriver
from selenium.webdriver.common.by import By
import sched,time,datetime
from variables import driver_path, username, password


browser = webdriver.Chrome(driver_path)
browser.get(('https://t.mmears.com/v2/home'))

# HTML elements
sign_in_button = browser.find_element_by_class_name("sign--26Rs4")
username_field = browser.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div[2]/div[1]/input')
password_field = browser.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div[2]/div[2]/input')
sign_in_submit = browser.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div[3]/div/div/div')
pop_up = browser.find_element_by_xpath('//*[@id="booknowWrapper"]/div[3]/div/div[2]/div/div/img')
confirm_button = browser.find_element_by_xpath('//*[@id="booknowWrapper"]/div[2]/div[2]/div[2]/div[1]')

sign_in_button.click()
username_field.send_keys(username)
password_field.send_keys(password)
sign_in_submit.click()
pop_up.click()


"""
def getDay():
    get a list of elements with classname 'wek-name'
    loop over each element
    if the node value of child element p == today's Day + 1 return div (that element's sibling)

def getClass():
    day = getDay()
    t = time.time()
    current_time = time.strftime("%H:%M", t)
    
    class_times = array of day's descendents whose classname == times
    loop over times_list
        if current_time < 06:00 && node value == "06:00 am"
            return ele
        if current_time > 06:00 && node value == "06:30 am"
            return ele
            
def sched_class(class, button):
    class.click()
    button.click()
    

class = getClass()

scheduler = sched.scheduler(time.sleep, time.sleep)

if time.time() < datetime.time(6,0,0): 
    scheduler.enterabs(datetime.time(6,0,0), 0, sched_class, argument=(class, confirm_button))
else:
    scheduler.enterabs(datetime.time(6,30,0), 0, sched_class, argument=(class, confirm_button))
    
scheduler.run()
"""