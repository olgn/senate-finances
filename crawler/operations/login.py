import time
from utils import env, urls # environment variables + shared selenium browser
from utils.browser import Keys
from selenium.common.exceptions import NoSuchElementException

def login(browser):
    # sets limit for how long
    # the browser will wait for an element on
    # the page to exist before 
    # throwing NoSuchElementException
    browser.implicitly_wait(10)
    
    # navigate to the login page
    browser.get(urls.LOGIN_URL)
    assert 'Instagram' in browser.title
    
    try:
        # attempt to login
        
        # enter username
        username_input = browser.find_element_by_name('username')
        username_input.send_keys(env.get('INSTAGRAM_USERNAME'))
        time.sleep(1)

        # enter password
        password_input = browser.find_element_by_name('password')
        password_input.send_keys(env.get('INSTAGRAM_PASSWORD'))
        time.sleep(1)

        # press enter
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
    except NoSuchElementException:
        # no such element on any of the previous workflow
        # means we're already logged in
        pass
    
    try:
        # tab twice and hit enter to dismiss notifications
        browser.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        time.sleep(1)
    except NoSuchElementException:
        # we have alreay dismissed notifications
        pass

    print('login sucessful!')