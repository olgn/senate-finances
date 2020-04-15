from utils import browser
from operations import agree, collect_ptr_links, collect_transactions, cleanup

agree(browser)

# collect all of the public transaction record links
# to investigate
collect_ptr_links(browser)

# crawl each public transaction record to populate
# the database with individual transactions
# associated with senator
collect_transactions(browser)

# then we cleanup on aisle 5
cleanup(browser)
