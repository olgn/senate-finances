import random
import time

def scroll(browser, scroll_range=20):
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    total_scrolls = random.randint(0, scroll_range)
    scroll_count = 0
    while scroll_count < total_scrolls:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(random.random() * 3)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        # increment scroll counter
        scroll_count+=1