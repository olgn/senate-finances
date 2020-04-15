from selenium.common.exceptions import StaleElementReferenceException

def sneaky_click(browser, element):
    try:
        browser.execute_script("arguments[0].click();", element)
    except StaleElementReferenceException:
        # page changes trigger this error
        pass