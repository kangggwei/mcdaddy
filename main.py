import pickle
from secrets import choice
from time import sleep
from display import GUI

try:
  with open('past_orders', 'rb') as f:
    past_orders = pickle.load(f)
except:
  past_orders = []

def open_menu(filename):
  with open(filename, 'rb') as f:
    menu = pickle.load(f)

  categories = []

  for section in menu:
    for name in section.keys():
      categories.append(name)

  # the list at the end contains keywords for beverages and desserts
  beverages = [category for category in categories if any(beverage in category.lower() for beverage in ['drinks', 'shake', 'iced'])]
  dessert = [category for category in categories if any(dessert in category.lower() for dessert in ['ice cream', 'sweet'])]
  food = [name for name in categories if name not in (beverages+dessert)]

  all_items = []
  beverage_list = []
  dessert_list = []
  food_list = []

  for section in menu:
    for name, item in section.items():
      all_items.extend(item)
      if name in beverages:
        beverage_list.extend(item)
      elif name in dessert:
        dessert_list.extend(item)
      else:
        food_list.extend(item)

  return (all_items, beverage_list, dessert_list, food_list)

def process(b, option, custom):
  def clean_list(options, budget):
    return [option for option in options if (float(option[1]) <= budget)]

  def mealify(options, budget):
    return [option for option in options if ('meal' in option[0].lower() and float(option[1]) <= budget)]

  def filter_list(item, selection):
    def isBeverage(item):
      return item[0] in [beverage[0] for beverage in beverage_list]

    def isDessert(item):
      return item[0] in [dessert[0] for dessert in dessert_list]

    def isDip(item):
      return 'Dip' in item[0][-3:]
  
    if isBeverage(item):
      return [item for item in selection if not isBeverage(item)]
    elif isDessert(item):
      return [item for item in selection if not isDessert(item)]
    elif isDip(item):
      return [item for item in selection if not isDip(item)]
    else:
      return selection

  def no_repeats(options, prev):
    return [option for option in options if option not in prev]

  def pick(options):
    order = choice(options)
    return order

  values=["I'm Feelin' Lucky", "Meals Only", "Breakfast"]

  if option not in values:
    print("If you want to be vegetarian, don't order from McDonald's")
    sleep(1)
    print("Shame on you")
    sleep(1)
    print("Loser")
    return
  elif option == values[2]:
    all_items, beverage_list, dessert_list, food_list = open_menu("breakfast")
  else:
    all_items, beverage_list, dessert_list, food_list = open_menu("menu")

  current_budget = b
  current_order = []
  current_menu = no_repeats(all_items, past_orders) if custom == 2 else all_items

  filter_func = mealify if option == values[1] else clean_list

  while current_budget > 0:
    selection = filter_func(current_menu, current_budget)
    if custom:
      selection = no_repeats(selection, current_order)
    if any(selection):
      selected = pick(selection)
      current_menu = filter_list(selected, selection)
      current_order.append(selected)
      current_budget -= float(selected[1])
    else:
      break

  for item, price in current_order:
    print(f"{item: <55}{'£'+price: >10}")

  total = str(round(b-current_budget,2))
  print('*'*65)
  sleep(1)
  print(f"{'TOTAL': <55}{'£'+total: >10}")

  with open('past_orders', 'wb') as f:
    past_orders.extend(current_order)
    pickle.dump(past_orders, f)

GUI(process)