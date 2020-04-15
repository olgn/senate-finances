import time
import datetime
import random
from selenium.common.exceptions import NoSuchElementException
import db
from utils import env, urls, scroll, sneaky_click
from utils.browser import Keys

def collect_data(browser, status='Current'):
    new_ptrs = 0

    # sort by date descending
    browser.find_element_by_xpath('//*[@id="filedReports"]/thead/tr/th[5]').click()

    # loop through all pages
    while True:
        try:
            # the way we know we reached the end is if there is a disabled next button
            browser.find_element_by_css_selector('a.next.disabled')
            print('inserted {} new ptr links into the database.'.format(new_ptrs))
            break
        except NoSuchElementException:
            # if there is not a disabled next button, then continue

            # loop through all the links on this page,
            # and if the page type is a transaction report,
            # add it to the database
            table = browser.find_element_by_id('filedReports')
            table_rows = table.find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
            
            for row in table_rows:
                # get the url of the report associated with each row
                tds = row.find_elements_by_tag_name('td')
                ptr_url = tds[-2].find_element_by_tag_name('a').get_attribute('href')

                # only collect links to ptr reports at this time
                # until we get some of that good good ocr computer vision shite
                if '/ptr/' in ptr_url:
                    
                    # parse first + middle from first name td
                    first_name = tds[0].text.upper().lstrip().rstrip()
                    middle_initial = None
                    if (len(first_name.split(' ')) > 1):
                        f = first_name.split(' ')
                        first_name = f[0]
                        middle_initial = f[-1]

                    # last name
                    last_name = tds[1].text.upper().lstrip().rstrip()
                    
                    # office
                    office = tds[2].text.upper()
                    
                    # submission date
                    date = tds[-1].text

                    associated_senator = db.get_senator(first_name, middle_initial, last_name, status)
                    if associated_senator is None:
                        senator_tuple = (
                            first_name, 
                            middle_initial,
                            last_name,
                            office,
                            status
                        )
                        senator_id = db.insert_senator(senator_tuple)
                    else:
                        senator_id = associated_senator['id']
                    
                    # construct ptr object
                    ptr_object = (
                        senator_id, # id of the associated senator
                        ptr_url, # senator ptr link
                        date # date the ptr was submitted 
                    )

                    # if we have not already crawled this row,
                    # add the ptr info to the database
                    if db.get_ptr(ptr_url) is None:
                        db.insert_ptr(ptr_object)
                        new_ptrs += 1
            
            # click the next button
            next_button = browser.find_element_by_css_selector('a.next')
            next_button.send_keys(Keys.RETURN)

def collect_ptr_links(browser):
    # sets limit for how long
    # the browser will wait for an element on
    # the page to exist before
    # throwing NoSuchElementException
    browser.implicitly_wait(3)

    print('Crawling senators to find associated reports...')
    
    # ~ loop through all senatorial candidates ~
    print('Collecting data on senatorial candidates...')
    browser.get(urls.SENATE_EFD_URL)

    # filter by senatorial candidates
    candidate_filter_checkbox = browser.find_element_by_class_name('candidate_filer').click()

    # click the search button
    search_button = browser.find_element_by_xpath('//*[@id="searchForm"]/div/button')
    sneaky_click(browser, search_button)
    time.sleep(2)

    collect_data(browser, 'Candidate')


    # ~ loop through all former senators ~
    print('Collecting data on former senators...')
    browser.get(urls.SENATE_EFD_URL)

    # filter by former senators
    candidate_filter_checkbox = browser.find_element_by_css_selector('#filerTypeLabelFormerSenator>input').click()

    # click the search button
    search_button = browser.find_element_by_xpath('//*[@id="searchForm"]/div/button')
    sneaky_click(browser, search_button)
    time.sleep(2)

    collect_data(browser, 'Former')

    # ~ loop through all senators ~
    print('Collecting data on current senators...')
    browser.get(urls.SENATE_EFD_URL) # go to home search page

    # filter by current senators
    senate_filter_checkbox = browser.find_element_by_class_name('senator_filer').click()

    # click the search button
    search_button = browser.find_element_by_xpath('//*[@id="searchForm"]/div/button')
    sneaky_click(browser, search_button)
    time.sleep(2)

    collect_data(browser, 'Current')
    print('Senator ptr link collection complete.')