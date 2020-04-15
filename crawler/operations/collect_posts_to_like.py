import time
import datetime
import random
from selenium.common.exceptions import NoSuchElementException
import db
from utils import env, urls, scroll
from utils.browser import Keys

def collect_posts_to_like(browser):
    # sets limit for how long
    # the browser will wait for an element on
    # the page to exist before
    # throwing NoSuchElementException
    browser.implicitly_wait(10)

    print('Crawling hashtags to find associated posts...')

    hashtags = env.get('HASHTAGS')
    if hashtags is None:
        print('No hashtags specified in config file. Exiting.')
        return

    # randomly shuffle the hashtags
    random.shuffle(hashtags)

    # loop through the hashtags
    # and crawl through the posts for a random length of time -
    # add new posts to the post database so
    # we can like em in the nest phase
    for hashtag in hashtags:
        # construct the hashtag url
        hashtag_url = '/'.join((urls.HASHTAG_URL, hashtag))

        # navigate to the hashtag url
        browser.get(hashtag_url)
        assert ''.join(('#', hashtag)) in browser.title

        # scroll down the page like a mindless zombie
        scroll(browser, 7)

        # grab a list of all the post urls associated with that hashtag
        posts = browser.find_elements_by_xpath('//a[contains(@href, "/p/")]')
        # print('found {} posts for hashtag #{}'.format(len(posts), hashtag))

        # keep a running tab of the new posts that were obtained in this crawl
        new_posts = 0
        for post in posts:
            post_url = post.get_attribute("pathname") # get the post url

            # create the post db entry
            post_object = (
                hashtag,
                post_url,
                # the created_date
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # if we have not already crawled this post,
            # add the post to the database
            if db.get_post(post_url) is None:
                db.insert_post(post_object)
                new_posts += 1

        print('inserted {} new posts into the database.'.format(new_posts))

        total_posts = db.count_posts_for_hashtag(hashtag)

        print('there are a total of {} associated with the hashtag #{}'.format(total_posts, hashtag))
