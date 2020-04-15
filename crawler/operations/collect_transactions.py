import time
import datetime
import random
from selenium.common.exceptions import NoSuchElementException
import db
from utils import env, urls, scroll, sneaky_click, string_strip
from utils.browser import Keys
from tqdm import tqdm

def collect_transactions(browser):

    print('Aquiring transaction history from each public transaction record...')
    # get all the public transaction records
    # from the database
    ptrs = db.get_all_active_ptrs()
    if ptrs is not None:

        # loop through each ptr entry and navigate to
        # the link
        for ptr in tqdm(ptrs):
            # go to url
            browser.get(ptr['url'])
            
            # get the table rows
            table_rows = browser.find_element_by_class_name('table').find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')

            for row in table_rows:
                tds = row.find_elements_by_tag_name('td')
                date = string_strip(tds[1].text)
                owner = string_strip(tds[2].text)
                ticker = string_strip(tds[3].text)
                asset_name = string_strip(tds[4].text)
                asset_type = string_strip(tds[5].text)
                transaction_type = string_strip(tds[6].text)
                transaction_amount = string_strip(tds[7].text)
                if (transaction_amount.find('Over') >= 0):
                    transaction_lower = string_strip(transaction_amount.split('Over')[1]).replace('$', '')
                    transaction_upper = None
                else:
                    transaction_lower = string_strip(transaction_amount.split('-')[0]).replace('$', '')
                    transaction_upper = string_strip(transaction_amount.split('-')[1]).replace('$', '')
                comment = string_strip(tds[8].text)

                transaction_tuple = (
                    ptr['id'], # id of the associated ptr
                    ptr['senator_id'], # id of the associated senator
                    owner, # name of owner of transaction
                    ticker, # ticker name (if applicable)
                    asset_name, # name of asset
                    asset_type, # type of asset
                    transaction_type, # type of transaction
                    transaction_lower, # lower bound of transaction amount
                    transaction_upper, # upper bound of transaction amount
                    comment, # associated comment on transaction
                    date # date of the transaction
                )

                db.insert_transaction(transaction_tuple)

            # set the ptr to 'collected'
            db.set_ptr_to_collected(ptr['id'])