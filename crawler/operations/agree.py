import time
from utils import env, urls, sneaky_click # environment variables + shared selenium browser
from utils.browser import Keys
from selenium.common.exceptions import NoSuchElementException

def agree(browser):
    # sets limit for how long
    # the browser will wait for an element on
    # the page to exist before 
    # throwing NoSuchElementException
    browser.implicitly_wait(10)
    
    # navigate to the login page
    browser.get(urls.SENATE_EFD_URL)
    assert 'eFD' in browser.title
    
    # agree and enter
    agree_input = browser.find_element_by_id('agree_statement')
    sneaky_click(browser, agree_input)
    
    try:
        # dismiss notifications if popup exists
        browser.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        time.sleep(1)
    except NoSuchElementException:
        # we have alreay dismissed notifications
        pass

    print('sucessfully agreed to unlawful usage notice')