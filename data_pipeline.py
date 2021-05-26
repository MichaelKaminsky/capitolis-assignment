import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger

from postgres_adapter import db

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run_data_pipeline():
    cron = BlockingScheduler(executors={'default': ThreadPoolExecutor(max_workers=1)})
    cron.add_job(daily_exchange_rates_etl, CronTrigger.from_crontab('0 16 * * MON-FRI'), coalesce=True)

    cron.start()


def daily_exchange_rates_etl():
    page = exchange_rates_request()
    logger.info('Requested to ecb-europa')
    exchange_rates = fetch_data(page)
    logger.info(f'Fetched {len(exchange_rates)} exchange rates')
    print(db.insert_rows(exchange_rates, 'public.exchange_rates'))
    logger.info('Sent to Postgres')


def exchange_rates_request():
    URL = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
    return requests.get(URL)


def fetch_data(page):
    exchange_rates = []
    soup = BeautifulSoup(page.content, 'html.parser')

    rate_date_text = soup.find(class_='jumbo-box').find('h3').text
    rate_date = datetime.strptime(rate_date_text, '%d %B %Y').date()
    week = rate_date.strftime("%W")

    currency_elems = soup.find(class_='forextable').find('tbody').find_all('tr')
    for currency_elem in currency_elems:
        currency_name = currency_elem.find('td', class_='currency').find('a').text
        currency_rate = currency_elem.find('span', class_='rate').text
        exchange_rates.append({'currency_name': currency_name,
                               'currency_rate_str': currency_rate,
                               'currency_rate_flt': currency_rate,
                               'rate_date': rate_date,
                               'week': week})
    return exchange_rates


run_data_pipeline()
# daily_exchange_rates_etl()