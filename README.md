# senate-finances
Electronic Financial Disclosure Scraper for Senate Records

## Setup
### Python
* install `virtualenv` and `python` 3.5+
* make a virtual environment with `python` 3.5+
* with `mkvirtualenv`, this looks like `mkvirtualenv -p python3 senate-finances`
* activate virtualenv - `workon senate-finances`
* install requirements - `cd crawler && pip install -r requirements.txt`

### Node.js
* install `node` 10+ and `yarn`
* install requirements - `cd visualizations && yarn && yarn start`

## Collecting data
Data is collected by scraping https://efdsearch.senate.gov/search
for financial records of current, former, and candidatorial senators

To crawl data, make sure python 3.5 is accessible and then `cd crawler && python main.py`

The dataset is stored in a file `db.sqlite` at the root of the repository.

The dataset contains the following tables:
* senators - a list of the first, last, and middle inital, as well as office of the senators in the dataset
* ptrs - a list of all the public transaction records (ptrs) urls that were submitted to the
eFD clearinghouse. each is linked to the senator that submitted
* transactions - a collection of all transactions that were found within the ptrs urls. show the individual asset exchanges reported by senators in their transaction record submissions.

A version of the dataset that was generated on 4.14.2020 is included in `db.sqlite`

***Note that this dataset only includes those trasaction records which were submitted in an electronic format. Further analysis that involves actually parsing pdf and handwritten documents is a next step, but will require a good deal more effort*** 