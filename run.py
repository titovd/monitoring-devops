import os
import logging
import time
import unicodedata
import graphyte


from selenium import webdriver
from bs4 import BeautifulSoup


logging.getLogger().setLevel(logging.INFO)
BASE_URL = 'https://www.blockchain.com/ru/prices'
GRAPHITE_HOST = 'graphite'


def parse_blockchain_data(page):
    coins_blocks = page.findAll('div', {'class': 'coin'})
    currencies_data = []

    bitcoin =  float(coins_blocks[0].find('p', {'title': 'Bitcoin'}).text[1:].replace(',', ''))
    ethereum =  float(coins_blocks[1].find('p', {'title': 'Ethereum'}).text[1:].replace(',', ''))
    xrp =  float(coins_blocks[2].find('p', {'title': 'XRP'}).text[1:].replace(',', ''))
    litecoin =  float(coins_blocks[3].find('p', {'title': 'Litecoin'}).text[1:].replace(',', ''))
    
    currencies_data.append(('Bitcoin', bitcoin))
    currencies_data.append(('Ethereum', ethereum))
    currencies_data.append(('XRP', xrp))
    currencies_data.append(('Litecoin', litecoin))

    return currencies_data


def send_metrics(currencies_data):
    sender = graphyte.Sender(GRAPHITE_HOST, prefix='currency')
    for currency in currencies_data:
        sender.send(currency[0], currency[1])


def main():

    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True}
    )

    driver.get(BASE_URL)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    metric = parse_blockchain_data(soup)
    send_metrics(metric)

    driver.quit()

    #logging.info(f'Accessed {BASE_URL} ..')
    #logging.info(f'Page title: {driver.title}')


if __name__ == '__main__':
    main()