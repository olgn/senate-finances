import time
import random
from selenium.common.exceptions import NoSuchElementException
import db
from utils import env, urls, scroll

def like_posts(browser):
    # get the max likes / hour
    likes_per_hour = env.get('LIKES_PER_HOUR')
    liked = 0

    if likes_per_hour is None:
        print('No likes per hour specified in the config file. Exiting.')
        return

    # use the likes / hour to determine the sleep time
    sleepy_time_mean = int(3600 / likes_per_hour)

    # get the hashtags we are looking for
    hashtags = env.get('HASHTAGS')
    if hashtags is None:
        print('No hashtags specified in config file. Exiting.')
        return

    # get the percentage of pages visited that we actually like
    # ... maybe ig cares about this?
    visited_to_liked_ratio = env.get('VISITED_TO_LIKED_RATIO')
    if visited_to_liked_ratio is None:
        # default this percentage to 40%
        visited_to_liked_ratio = 0.4

    # collect the posts that have not already been liked for each
    # hashtag
    posts = []
    for hashtag in hashtags:
        # query the database for entries with that hashtag value +
        # liked == False
        unliked_posts = db.get_unliked_posts(hashtag)

        # add these unliked posts to a master list of unliked posts
        # for all hashtags
        posts += unliked_posts

    # print('found {} fresh posts to like for all hashtags.'.format(len(posts)))

    random.shuffle(posts) # shuffle the posts

    # loop through the posts
    for post in posts:

        # roll the dice and don't do anything with the post
        # if visited_to_liked_ratio is > dice roll
        if random.random() <= visited_to_liked_ratio:
            print('passing...')
            continue

        # go to the post url
        try:
            post_url = '{}{}'.format(urls.INSTAGRAM_URL, post.get("url"))
            browser.get(post_url)

            # find the like button
            like_button = browser.find_element_by_xpath('//span[@aria-label="Like"]')

            # make it look like u actually care about the page
            # by sleeping for a while...
            sleep_for = max(1, random.gauss(sleepy_time_mean, 3))
            print('sleeping for {} seconds...'.format(sleep_for))
            time.sleep(sleep_for)

            # click the like button
            like_button.click()

            # update the database entry to show that the post has
            # been liked
            db.set_post_liked(post.get('url'))

            # increment post counter
            liked +=1

            # check to make sure we're not over the limit
            if liked > sleepy_time_mean:
                # if we are, break this cycle
                return

        except NoSuchElementException:
            # no such element means the like button isn't on the page,
            # so the post is likely deleted.
            # we should remove it from the database
            print('couldnt find the like button... assuming post is gone. Removing entry from database.')
            db.delete_post(post.get('url'))

    return
