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
        """
        Get item information from the Guild Wars 2 API.
        :param number: The id number of the item
        :return: The best buy and sell prices or None if not available
        """
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
        """
        :param number: Item number to be looked up.
        :return: Item information in json.
        """
        item_url = "https://api.guildwars2.com/v2/items/{}".format(number)
        return requests.get(item_url).json()

    def display(self):
        """
        The main Item method. Call to print information.
        :return: Prints out all of the details and price information
        for an item.
        """
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

        # For testing, probably not needed.
        return self.number


class Recipe:

    def __init__(self, num):
        self.num = num
        self.output_sell_price = 0
        self.ingredients_cost = 0

    @staticmethod
    def get_recipe(num):
        """
        :param num: Recipe id number.
        :return: Recipe information in json.
        """
        recipe_url = "https://api.guildwars2.com/v2/recipes/{}".format(num)
        recipe = requests.get(recipe_url)

        return recipe.json()

    @staticmethod
    def get_item(num):
        """
        This is used for both output and ingredient items.
        :param num: Item id number.
        :return: Item information in json.
        """
        item_url = "https://api.guildwars2.com/v2/items/{}".format(num)
        item_info = requests.get(item_url)
        return item_info.json()

    @staticmethod
    def get_prices(num):
        """
        :param num: Item number.
        :return: Buy and sell price information for the given number.
        """
        price_url = "https://api.guildwars2.com/v2/commerce/prices/{}"\
            .format(num)
        lookup = requests.get(price_url)
        prices = lookup.json()

        if "buys" in prices:
            buy = prices["buys"]["unit_price"]
            sell = prices["sells"]["unit_price"]
            return buy, sell
        else:
            return None

    def output_item_display(self, number):
        """
        :param number: Output item id number.
        :return: Prints information for a recipe output item.
        """
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
        """
        :param price: Price * quantity for one ingredient.
        :return: Updates total cost of ingredients.
        """
        self.ingredients_cost += price

    def display_ingredient(self, num, quantity):
        """
        :param num: Id number for one ingredient.
        :param quantity: Quantity of item used in recipe.
        :return: Total cost for a single ingredient item.
        """
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
        """
        This is the main Recipe display method.
        :return: Prints recipe information including ingredients,
        output item, ingredients, and costs.
        """
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

        return self.num


class Main:

    @staticmethod
    def number_input(choice):
        """
        This method looks up a list of all available id numbers for
        either recipes or items.
        :param choice: User input choosing to lookup recipes or items.
        :return: A list of all available id numbers.
        """
        option_string = "https://api.guildwars2.com/v2/{}/"

        if choice == "R":
            url_string = option_string.format("recipes")
        else:
            url_string = option_string.format("items")

        options = requests.get(url_string).json()
        return options

    @staticmethod
    def get_id_input(options):
        """
        Prompts user to input a valid id number to look up. Only to highest
        and lowest numbers are listed. An unavailable selection will
        repeat the prompt.
        :param options: All available id numbers.
        :return: Valid id number to be looked up.
        """
        lowest = min(options)
        highest = max(options)
        number = " "
        while not number.isnumeric() or int(number) not in options:

            print("Please enter an id from {} to {}".format(lowest, highest))
            number = input(":: ")
        return int(number)

    @staticmethod
    def create_object(choice, id_num):
        """
        :param choice: Type of object to be instantiated.
        :param id_num: Id number to be instantiated.
        :return: An object to Main to be displayed.
        """
        if choice == "R":
            return Recipe(id_num)
        else:
            return Item(id_num)

    def run(self):
        """
        The main run function. The user selects a type of object, a specific
        number, and then the corresponding information is displayed.
        :return: The object information is printed. User is prompted to make
        another selection.
        """
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
