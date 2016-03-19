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
        if "buys" in prices:
            buys = [int(x["unit_price"]) for x in prices["buys"]]
            sells = [int(x["unit_price"]) for x in prices["sells"]]
            highest_buy = max(buys)
            lowest_sell = min(sells)
            return highest_buy, lowest_sell
        else:
            return None

    @staticmethod
    def get_info(number):
        item_url = "https://api.guildwars2.com/v2/items/{}".format(number)
        return requests.get(item_url).json()

    def display(self):
        info = self.get_info(self.number)

        print("")
        for area in self.basic_fields:
            print(area, info.get(area, "NA"), sep=": ")

        print("details: ")
        for k, v in info["details"].items():
            print("\t{}: {}".format(k, v))

        prices = self.get_prices(self.number)

        if prices is None:
            print("Soulbound, no prices")
        else:
            print("highest buy price: ", prices[0])
            print("lowest sell price: ", prices[1])
            print("price spread: ", prices[1] - prices[0])


class Recipe:

    def __init__(self, num):
        self.num = num
        self.output_sell_price = 0
        self.ingredients_cost = 0

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

        if "buys" in prices:
            buy = prices["buys"]["unit_price"]
            sell = prices["sells"]["unit_price"]
            return buy, sell
        else:
            return None

    def output_item_display(self, number):
        # return info on an output item to be printed by display.
        item = self.get_item(number)
        areas = ["name", "rarity", "vendor_value"]

        for area in areas:
            print("{}: {}".format(area, item[area]))

        prices = self.get_prices(number)

        if prices:
            # Store price for later calc.
            self.output_sell_price = prices[1]

            print("buy price: {}".format(prices[0]))
            print("sell price: {}".format(prices[1]))
        else:
            self.output_sell_price = None
            print("Item is bound, no selling")

    def update_ingredient_cost(self, price):
        self.ingredients_cost += price

    def display_ingredient(self, num, quantity):
        # Not sure if None check is needed, just to be safe.

        ingredient_info = self.get_item(num)
        print("name: {}".format(ingredient_info["name"]))
        print("rarity: {}".format(ingredient_info["rarity"]))
        print("quantity: {}".format(quantity))

        prices = self.get_prices(num)

        if prices:
            buy = int(prices[0])

            print("unit price: {}".format(buy))

            total_price = buy * quantity
            print("total price: {}\n".format(total_price))

            self.update_ingredient_cost(total_price)

        else:
            print("Bound item, can not be sold")

    def display(self):
        # main display method, draws info from other methods.
        # calc price difference.
        recipe = self.get_recipe(self.num)
        output_id = recipe["output_item_id"]

        print("\nid number: {}".format(self.num))
        print("recipe type: {}\n".format(recipe["type"]))

        print("\nOutput Item:")
        self.output_item_display(output_id)
        print("Items produced: {}".format(recipe["output_item_count"]))
        print("Minimum item rating: {}".format(recipe["min_rating"]))

        print("-" * 100)
        print("\nIngredients\n")
        for ingredient in recipe["ingredients"]:
            item_id = ingredient["item_id"]
            quantity = ingredient["count"]
            self.display_ingredient(item_id, quantity)

        if self.output_sell_price is None:
            print("Bound item, no price difference")
        else:
            price_diff = self.output_sell_price - self.ingredients_cost
            print("Price difference: {}\n".format(price_diff))


class Main:

    # def __int__(self):
    #     self.keep_going = True

    @staticmethod
    def number_input(choice):
        option_string = "https://api.guildwars2.com/v2/{}/"

        if choice == "R":
            url_string = option_string.format("recipes")
        else:
            url_string = option_string.format("items")

        options = requests.get(url_string).json()
        return options

    @staticmethod
    def get_id_input(options):
        lowest = min(options)
        highest = max(options)
        number = " "
        while not number.isnumeric() or int(number) not in options:

            print("Please enter an id from {} to {}".format(lowest, highest))
            number = input(":: ")
        return int(number)

    @staticmethod
    def create_object(choice, id_num):
        if choice == "R":
            return Recipe(id_num)
        else:
            return Item(id_num)

    def run(self):
        print("Welcome to the Guild Wars 2 API")
        print("What do you want to look up?")

        running = True
        while running:
            choice = input("\n[I]tem\n[R]ecipe\n[Q]uit\n:: ").upper()
            if choice == "Q":
                running = False

            if choice in "RI":
                options = self.number_input(choice)
                id_num = self.get_id_input(options)

                active_object = self.create_object(choice, id_num)
                active_object.display()


if __name__ == '__main__':
    main = Main()
    main.run()

