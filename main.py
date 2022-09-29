import requests
from bs4 import BeautifulSoup
import logging
import telegram
#from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
token = '******'
lots=[]

def parser():
    URL = "https://www.avito.ru/moskva/odezhda_obuv_aksessuary/kupit-verhnyaya_odezhda-muzhskaya_odezhda" \
          "-ASgBAgICAkTeAtgL4ALeCw?cd=1&q=stone+island+куртка&s=104 "
    USER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36',
        'accept': '*/*'}
    response = requests.get(URL, headers=USER)
    #page`s code
    soup = BeautifulSoup(response.text, "lxml")
    # print(soup)
    # lots = {}

    fiveLast= soup.find_all('div', class_='iva-item-body-NPl6W').text
    for item in fiveLast:

        block = soup.find('div', class_='iva-item-body-NPl6W')

        title = block.find('a', class_='link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj'
                                       'title-listRedesign-3RaU2 title-root_maxHeight-3obWc').get("title")
        link = block.find('a', class_='link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj '
                                      'title-listRedesign-3RaU2 title-root_maxHeight-3obWc').get('href')
        price = block.find('span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').text

        lots.append(title + '(' + price + ')'+' '+'https://www.avito.ru/' + link)
        #lots.update({title + '(' + price + ')':'https://www.avito.ru/' + link})

def shownews(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(lots)


def main() -> None:
    parser()
    print(lots)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", shownews))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
