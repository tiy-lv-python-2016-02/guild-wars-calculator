import requests
import pprint
import sys


# should be item
class ItemRequest:

    item_properties = [
            'name', 'id', 'description', 'type',
            'rarity', 'level', 'vendor_value',
            'game_types', 'restrictions', 'details'
    ]


    @staticmethod
    def item_input(items_list):
        """
        user gives id number
        :param items_list: the list of available items
        with listings.
        """
        id_input = None

        while not id_input:
            print('\n')
            id_input = \
                input("Enter item ID number: >> 1 - 78005 >> :  ")

            if int(id_input) not in items_list:
                print("\nSorry. Invalid ID.")
                id_input = None
        return int(id_input)

    @staticmethod
    def item_request(id_num):
        """
        uses id number input to request
        the item's properties
        :param id_num:  id input by user
        """
        # item_properties = [
    #         'name', 'id', 'description', 'type',
    #         'rarity', 'level', 'vendor_value',
    #         'game_types', 'restrictions', 'details'
    # ]
        item_request = \
            requests.get("https://api.guildwars2.com/v2/items/{}"
                         .format(id_num))
        item_dict = item_request.json()
        item = ItemRequest()
        for key in ItemRequest.item_properties:
            setattr(item, key, item_dict.get(key))

        return item

    def details_format(self):
        """
        formats the details from the pulled item details
        """
        for key in self.item_properties:
            if key == 'details':
                print(key, ": ")
                pprint.pprint(self.details)
            else:
                print(key,":", getattr(self, key, None))


class Listing:

    def __init__(self, id_number):
        self.id = str(id_number)

    @staticmethod
    def listing_request(id_number):
        listing_request =\
            requests.get("https://api.guildwars2.com/v2/commerce/listings/{}"
                     .format(id_number))
        listing_dict = listing_request.json()

        return listing_dict

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

    recipe_properties = [
        'id', 'type', 'output_item_count',
        'output_item_id', 'min_rating', 'ingredients'
    ]

    def __init__(self):
        """
        recipe input set at none to enable
        user input function
        """
        self.ingredients_list = []

    @staticmethod
    def user_input(recipe_ids):
        """
        gets recipe id number user
        wants to look up
        """
        recipe_input = None
        while not recipe_input:
            recipe_input = input("Enter item id to get the recipe: ")
            print("\n")

            if int(recipe_input) not in recipe_ids:
                print("\nSorry. Not a valid recipe id.")
                recipe_input = None

        return int(recipe_input)

    @staticmethod
    def recipe_request(id_number):

        recipe_request = \
            requests.get("https://api.guildwars2.com/v2/recipes/{}"
                         .format(id_number))

        recipe_dict = recipe_request.json()
        recipe = Recipe()
        for key in Recipe.recipe_properties:
            setattr(recipe, key, recipe_dict.get(key))

        return recipe

    def details_format(self):
        """
        formats the details from the pulled item details
        """
        for key in self.recipe_properties:
            print(key,":", getattr(self, key, None))

    def ingredient_list(self):

        total_ingredient_cost = []

        for ingredient in self.ingredients:

            item_id = ingredient.get('item_id')

            quantity = int(ingredient.get('count'))

            ingredient_pull = ItemRequest.item_request(int(item_id))

            ingredient_pull.details_format()

            each = Price.price_request(item_id)

            pricing = Price.price_request(item_id) * quantity

            print("Total cost of ingredient: {}.\n({} x {}(quantity))."
                  .format(pricing, each, quantity))

            total_ingredient_cost.append(pricing)

            print('\n')

        return total_ingredient_cost


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


def main_menu():
    """
    main menu of the program.
    user is given option to
    look up a recipe or item,
    with option to quit
    """
    option_input = None

    while not option_input:
        print("What are you trying to look up?")
        option_input = input("(R)ECIPE OR (I)TEM?"
                             "(*Type (Q) to quit.)\n>>").lower()

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

    all_listing_ids = requests.get\
        ("https://api.guildwars2.com/v2/commerce/listings/")
    all_recipes = requests.get\
        ("https://api.guildwars2.com/v2/recipes/")

    recipe_ids = all_recipes.json()
    items_with_listing = all_listing_ids.json()


    output_properties = [
        'name', 'rarity',
        'level', 'vendor_value',
    ]

    ingredient_properties = [
        'name', 'rarity'
    ]

    main = main_menu()

    while main in 'ri':

        if main in "r":

            id_number = Recipe.user_input(recipe_ids)
            recipe_pulled = Recipe.recipe_request(id_number)

            recipe_pulled.details_format()

            print("\n------------OUTPUT ITEM DETAILS-------------")

            recipe_output = int(recipe_pulled.output_item_id)

            recipe_details = ItemRequest.item_request(recipe_output)

            ItemRequest.details_format(recipe_details)

            recipe_listings = Listing.listing_request(recipe_output)

            print('\n------------INGREDIENTS DETAILS-------------')

            total_ingredient_cost = recipe_pulled.ingredient_list()

            print("TOTAL COST FOR OUTPUT ITEM : {}\n"
                  .format(sum(total_ingredient_cost)))
            output_item = ItemRequest.item_request(recipe_output)

            crafting_difference = Listing.lowest_sell(recipe_listings)- \
                                  sum(total_ingredient_cost)

            print("PRICE DIFFERENCE CRAFTING VS BUYING FROM TRADE POST::"
                  "\n{}".format(crafting_difference))

        if main in 'i':

            item_number = ItemRequest.item_input(items_with_listing)

            item_pulled = ItemRequest.item_request(item_number)
            item_pulled.details_format()

            item_listing = Listing.listing_request(item_number)
            Listing.price_listings(item_listing)

        main = main_menu()
