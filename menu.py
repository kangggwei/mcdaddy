from requests import get
from lxml import html
from dotenv import load_dotenv
import pickle
import os

load_dotenv()

def load_menu(url, filename):
  # get response from the website
  response = get(url)
  # convert the response to html to sieve out menu items
  tree = html.fromstring(response.content)

  menu = []
  counter = 1

  while True:
    try:
      section = []
      category_name = tree.xpath(f'//*[@id="main-content"]/div[3]/ul/li[{counter}]/h2/text()')[0]
      item = 1
      while True:
        try:
          name = tree.xpath(f'//*[@id="main-content"]/div[3]/ul/li[{counter}]/ul/li[{item}]/div/div/div/div[1]/div[1]/h4/div/text()')[0]
          price = tree.xpath(f'//*[@id="main-content"]/div[3]/ul/li[{counter}]/ul/li[{item}]/div/div/div/div[1]/div[3]/div/text()')[0][1:]
          item += 1
          if price[0].isalpha():
            continue
          section.append((name, price))
        except:
          break
      menu.append({category_name: section})
      counter += 1
    except:
      break

  # saving the menu to pickle
  with open(filename, 'wb') as f:
    pickle.dump(menu, f)

load_menu(os.environ["BREAKFAST_URL"], 'breakfast')
load_menu(os.environ["LUNCH_URL"], 'menu')