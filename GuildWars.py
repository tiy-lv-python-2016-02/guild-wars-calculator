import requests


class Item:

    def __init__(self, number):
        self.number = number
        self.basic_fields = ['name', 'id', 'description', 'type', 'rarity',
                             'level', 'vendor_value', 'game_types',
                             'restrictions'
                             ]

    @staticmethod
    def get_prices(number):
        price_string = "https://api.guildwars2.com/v2/commerce/" \
                            "listings/{}".format(number)
        listing = requests.get(price_string)
        prices = listing.json()
        buys = [int(x["unit_price"]) for x in prices["buys"]]
        sells = [int(x["unit_price"]) for x in prices["sells"]]
        highest_buy = max(buys)
        lowest_sell = min(sells)
        return highest_buy, lowest_sell

    @staticmethod
    def get_info(number):
        item_url = "https://api.guildwars2.com/v2/items/{}".format(number)
        return requests.get(item_url).json()

    def display(self):
        info = self.get_info(self.number)
        prices = self.get_prices(self.number)

        print("")
        for area in self.basic_fields:
            print(area, info[area], sep=": ")

        print("details: ")
        for k, v in info["details"].items():
            print("\t{}: {}".format(k, v))

        print("highest buy price: ", prices[0])
        print("lowest sell price: ", prices[1])
        print("price spread: ", prices[1] - prices[0])


class Recipe:

    def __init__(self, num):
        self.num = num
        self.output_sell_price = 0
        self.ingredient_cost = 0

    @staticmethod
    def get_recipe(num):
        recipe_url = "https://api.guildwars2.com/v2/recipes/{}".format(num)
        recipe = requests.get(recipe_url)

        return recipe.json()

    @staticmethod
    def get_item(num):
        # gets info for item
        # used for both output and ingredients
        item_url = "https://api.guildwars2.com/v2/items/{}".format(num)
        item_info = requests.get(item_url)
        return item_info.json()

    @staticmethod
    def get_prices(num):
        # get buy/sell price for item
        # https://api.guildwars2.com/v2/commerce/prices/{}
        price_url = "https://api.guildwars2.com/v2/commerce/prices/{}".format(num)
        lookup = requests.get(price_url)
        prices = lookup.json()
        buy = prices["buys"]["unit_price"]
        sell = prices["sells"]["unit_price"]
        return buy, sell

    def output_item_display(self):
        # return info on an output item to be printed by display.
        item = self.get_item(self.num)
        areas = ["name", "rarity", "vendor_price"]

        for area in areas:
            print("{}: {}".format(area, item[area]))

        prices = self.get_prices(self.num)

        # Store price for later calc.
        self.output_sell_price = prices[1]

        print("buy price: {}".format(prices[0]))
        print("sell price: {}".format(prices[1]))

    def ingredient_item(self):
        # return info on an ingredient item to be printed by display.

        pass

    def display_ingredients(self):
        # Need the buy price of all ingredients for each item

        pass

    def display(self):
        # main display method, draws info from other methods.
        # calc price difference.
        recipe = self.get_recipe(self.num)
        print(self.num, recipe["type"], sep="\n")

        print("")
        print("Output Item:")
        self.output_item_display()
        print(recipe["output_item_count"])
        print(recipe["min_rating"])

        # Output item displayed, move on to ingredients.







number = 28445

item = Item(number)

item.display()








