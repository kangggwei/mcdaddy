from requests import get
from lxml import html
import pickle

url = # insert ubereats URL here

# get response from the website
response = get(url)
# convert the response to html to sieve out menu items
tree = html.fromstring(response.content)

menu = []
# there are 17 categories in the macdonalds menu so we iterate until from 1 to 17
for category in range(3, 18):
  section = []
  category_name = tree.xpath(f'//*[@id="main-content"]/div[3]/ul/li[{category}]/h2/text()')[0]
  item = 1
  while True:
    try:
      name = tree.xpath(f'//*[@id="main-content"]/div[3]/ul/li[{category}]/ul/li[{item}]/div/div/div/div[1]/div[1]/h4/div/text()')[0]
      price = tree.xpath(f'//*[@id="main-content"]/div[3]/ul/li[{category}]/ul/li[{item}]/div/div/div/div[1]/div[3]/div/text()')[0][1:]
      item += 1
      if price[0].isalpha():
        continue
      section.append((name, price))
    except:
      break
  menu.append({category_name: section})

# saving the menu to pickle
with open('menu', 'wb') as f:
  pickle.dump(menu, f)
