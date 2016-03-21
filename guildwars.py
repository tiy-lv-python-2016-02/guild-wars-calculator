import requests
import pprint
import sys


class ItemRequest:

    def __init__(self):
        """
        id_input starting at none to enable the while loop in
        input function
        """

        self.id_input = None

    def item_input(self, items_list):
        """
        user gives id number
        :param items_list: the list of available items
        with listings.
        """
        while self.id_input is None:
            print('\n')
            self.id_input = \
                input("Enter item ID number: >> 1 - 78005 >> :  ")

            if int(self.id_input) not in items_list:
                print("\nSorry. Invalid ID.")
                self.id_input = None
        return int(self.id_input)

    @staticmethod
    def item_request(id_num):
        """
        uses id number input to request
        the item's properties
        :param id_num:  id input by user
        """
        item_request = \
            requests.get("https://api.guildwars2.com/v2/items/{}"
                         .format(id_num))
        item = item_request.json()
        return item

    @staticmethod
    def details_format(dictionary_pulled, properties_wanted):
        """
        formats the details from the pulled item details
        :param dictionary_pulled: item or recipe details
        :param properties_wanted: list of properties to be pulled
        """

        for key in properties_wanted:
            if key == 'details':
                print(key, ": ")
                pprint.pprint(dictionary_pulled['details'])
            else:
                print(key,":", dictionary_pulled.get(key, "None"))


class Listing:

    def __init__(self, id, listing):
        self.id = str(id)
        self.listing_requested = listing

    @staticmethod
    def listing_request(id_number):
        listing_request =\
            requests.get("https://api.guildwars2.com/v2/commerce/listings/{}"
                     .format(id_number))
        listing = listing_request.json()
        return listing

    @staticmethod
    def price_listings(listing_requested):
        """
        shows highest buy listing and lowest sell listing
         of item requested
        :param listing_requested:  id number of item
        requested by user
        """

        # listings are priced in ascending order from lowest to highest.

        print("HIGHEST BUY ORDER LISTING(S):")
        pprint.pprint(listing_requested.get('buys')[-1])

        highest_buy = listing_requested.get('buys')[-1]['unit_price']

        print("LOWEST SELL OFFER LISTING(S):")
        pprint.pprint(listing_requested.get('sells')[0])

        lowest_sell = listing_requested.get('sells')[0]['unit_price']

        price_spread = lowest_sell - highest_buy
        print("PRICE SPREAD:")
        print(price_spread)

    @staticmethod
    def lowest_sell(listing_requested):
        """
        shows lowest sell listing
        mostly used to compare recipe crafted item
        cost vs trade post cost
        :param listing_requested: id number of requested
        item
        """
        print("LOWEST SELL OFFER LISTING(S):")
        pprint.pprint(listing_requested['sells'][0])

        return listing_requested['sells'][0]['unit_price']


class Recipe:

    def __init__(self):
        """
        recipe input set at none to enable
        user input function
        """
        self.recipe_input = None

    def user_input(self):
        """
        gets recipe id number user
        wants to look up
        """
        while self.recipe_input is None:
            self.recipe_input = input("Enter item id to get the recipe: ")
            print("\n")

            if int(self.recipe_input) not in recipe_ids:
                print("\nSorry. Not a valid recipe id.")
                self.recipe_input = None

        return int(self.recipe_input)

    @staticmethod
    def recipe_request(id_number):

        recipe_request = \
            requests.get("https://api.guildwars2.com/v2/recipes/{}"
                         .format(id_number))

        recipe = recipe_request.json()

        return recipe


class Price:

    def __init__(self, id_num):
        self.id = id_num

    @staticmethod
    def price_request(id_num):
        """
        returns current aggregated buy and sell listing
        information from the trading post.
        used in this program ingredient's cost
        """
        price_request = requests.get\
            ("https://api.guildwars2.com/v2/commerce/prices/{}"
                                     .format(id_num))
        price = price_request.json()
        return price['buys']['unit_price']


class GW2Main:

    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        """
        main menu of the program
        user is given option to
        look up a recipe or item,
        with option to quit
        :return:
        """
        option_input = None

        while option_input is None:
            print("What are you trying to look up?")
            option_input = input("(R)ECIPE OR (I)TEM? (*Type (Q) to quit.)\n>>").lower()

            if option_input not in "riq":

                print("Sorry. Invalid Input.")
                option_input = None

            elif option_input == "q":

                sys.exit()

        return option_input

if __name__ == '__main__':

    print("..............................................\n")
    print("              WELCOME TO THE")
    print("\nGUILD WARS 2 ITEM AND RECIPE PRICE CALCULATOR\n")
    print("..............................................\n")
    print("      ...LOADING AVAILABLE ITEMS...\n")

    all_listing_ids = requests.get("https://api.guildwars2.com/v2/commerce/listings/")
    all_recipes = requests.get("https://api.guildwars2.com/v2/recipes/")

    recipe_ids = all_recipes.json()
    items_with_listing = all_listing_ids.json()

    item_properties = [
            'name', 'id', 'description', 'type',
            'rarity', 'level', 'vendor_value',
            'game_types', 'restrictions', 'details'
    ]

    recipe_properties = [
        'id', 'type', 'output_item_count',
        'min_rating'
    ]

    output_properties = [
        'name', 'rarity',
        'level', 'vendor_value',
    ]

    ingredient_properties = [
        'name', 'rarity'
    ]

    main = GW2Main.main_menu()
    while main in 'ri':
        if main in "r":
                recipe = Recipe()

                id_number = recipe.user_input()
                recipe_pulled = Recipe.recipe_request(id_number)

                ItemRequest.details_format(recipe_pulled, recipe_properties)
                recipe_output = int(recipe_pulled['output_item_id'])

                print("\n------------OUTPUT ITEM DETAILS-------------")
                recipe_details = ItemRequest.item_request(recipe_output)
                ItemRequest.details_format(recipe_details, output_properties)
                recipe_listings = Listing.listing_request(recipe_output)

                print('\n------------INGREDIENTS DETAILS-------------')
                total_ingredient_cost = []

                for x in recipe_pulled['ingredients']:

                    item_id = x.get('item_id')

                    quantity = int(x.get('count'))

                    ingredient_pull = ItemRequest.item_request(int(item_id))

                    ItemRequest.details_format(ingredient_pull,
                                               ingredient_properties)

                    each = Price.price_request(item_id)

                    pricing = Price.price_request(item_id) * quantity

                    print("Total cost of ingredient: {}.\n({} x {}(quantity))."
                          .format(pricing, each, quantity))

                    total_ingredient_cost.append(pricing)

                    print('\n')

                print("TOTAL COST FOR OUTPUT ITEM :: {}\n".format(sum(total_ingredient_cost)))
                output_item = ItemRequest.item_request(recipe_output)

                crafting_difference = Listing.lowest_sell(recipe_listings) - \
                                      sum(total_ingredient_cost)
                print("PRICE DIFFERENCE CRAFTING VS BUYING FROM TRADE POST::"
                      "\n{}".format(crafting_difference))

                main = GW2Main.main_menu()
        if main in 'i':

            item = ItemRequest()

            item_number = item.item_input(items_with_listing)

            item_pulled = item.item_request(item_number)
            ItemRequest.details_format(item_pulled, item_properties)

            item_listing = Listing.listing_request(item_number)
            Listing.price_listings(item_listing)

            main = GW2Main.main_menu()
