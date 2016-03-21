import requests


class Item:
    """
    This class could be laid out much better. The Recipe and Character
    classes each look up item information. This class should handle all item
    lookups. Recipe and Character could instantiate an Item object and
    get the information they need through that object.
    """

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

        # For testing
        return self.number


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
        item_url = "https://api.guildwars2.com/v2/items/{}".format(num)
        item_info = requests.get(item_url)
        return item_info.json()

    @staticmethod
    def get_prices(num):
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


class Character:

    # I should refactor the Item class to do this lookup and the
    # item lookups in the Recipe class.
    item_url = "https://api.guildwars2.com/v2/items/{}"

    def __init__(self, url):
        self.url = url
        self.info = requests.get(self.url).json()
        self.name = self.info.get("name", "")
        self.race = self.info.get("race", "")
        self.prof = self.info.get("profession", "")
        self.intro = "{}/{}/{}".format(self.name, self.race, self.prof)
        self.vendor_value = None

    def print_intro(self):
        print(self.intro)

    def item_value(self, iid):
        """
        :param iid: Item id number
        :return: Vendor value of the item. 0 if no value listed.
        """
        item = requests.get(self.item_url.format(iid)).json()
        return item.get("vendor_value", 0)

    def get_inventory(self):
        """
        :return: Splices "/inventory" into the get request and returns
        the character's inventory json.
        """
        url_split = self.url.split("?access_token")
        new = "{}/inventory?access_token{}".format(url_split[0], url_split[1])
        inventory = requests.get(new).json()
        return inventory

    def set_vendor_value(self, inventory):
        """
        :param inventory: List of all character inventory items.
        :return: Sets self.vendor_value to the total inventory value.
        """
        bags = inventory["bags"][0]["inventory"]

        value = 0
        for bag in bags:
            if bag and "id" in bag and "count" in bag:
                val = self.item_value(bag["id"])
                count = bag["count"]
                value += val * count
        self.vendor_value = value

    def display(self):
        """
        :return: Prints the value of all character items.
        """
        if self.vendor_value is None:
            inventory = self.get_inventory()
            self.set_vendor_value(inventory)
        print("The vendor value of all inventory items is: {}".format(
            self.vendor_value)
        )


class Game:

    def __init__(self, api_key):
        self.items = {}
        self.recipes = {}
        self.characters = {}
        self.api_key = api_key

        self.base_url = "https://api.guildwars2.com/v2/characters{}?" \
                        "access_token={}"
        self.char_url = self.base_url.format("", self.api_key)
        self.char_list = requests.get(self.char_url).json()

        for name in self.char_list:
            char = Character(self.base_url.format("/" + name, self.api_key))
            self.characters[char.intro] = char

    def display_chars(self):
        for c in self.characters:
            self.characters[c].print_intro()

    def select_char(self):
        # Return chosen character lookup key.

        selection = ""
        char_intros = list(self.characters.keys())  # List of character keys.
        for i, k in enumerate(char_intros):
            print("{}: {}".format(i+1, k))

        numbers = range(1, len(char_intros) + 1)
        while not selection.isnumeric() or int(selection) not in numbers:
            selection = input("Please select a player number: ")

        chosen_key = char_intros[int(selection)-1]
        return chosen_key

    def number_input(self, choice):
        option_string = "https://api.guildwars2.com/v2/{}/"
        if choice == "C":
            self.display_chars()

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

    def update_cache(self, choice, id_num, instance):
        if choice == "I":
            self.items[id_num] = instance
        elif choice == "R":
            self.recipes[id_num] = instance
        elif choice == "C":
            self.characters[id_num] = instance
        else:
            pass

    def lookup_cache(self, choice, id_num):
        if choice == "I":
            return self.items.get(id_num, None)
        elif choice == "R":
            return self.recipes.get(id_num, None)
        elif choice == "C":
            return self.characters.get(id_num, None)
        else:
            return None

    def run(self):
        print("Welcome to the Guild Wars 2 API")
        print("What do you want to look up?")

        choice = ""
        while choice != "Q":
            print("\n[I]tem\n[R]ecipe\n[C]har")
            self.display_chars()
            choice = input("\n[Q]uit\n:: ").upper()

            if choice in "RIC":
                options = self.number_input(choice)

                if choice == "C":
                    id_num = self.select_char()
                else:
                    id_num = self.get_id_input(options)

                active_object = self.lookup_cache(choice, id_num)

                if active_object is None:

                    active_object = self.create_object(choice, id_num)
                    self.update_cache(choice, id_num, active_object)

                active_object.display()


if __name__ == '__main__':
    API_KEY = "8A087585-4C99-1A43-839C-EEDABC86FD4EB7AC59A0-2956-4BE9-8FB3-" \
              "DF4B7AE7BCA0"

    main = Game(API_KEY)
    main.run()
