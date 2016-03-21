from unittest import TestCase
from GuildWars import Recipe, Item


class ItemTests(TestCase):
    """
    This test looks up many different item id numbers to check that there
    are no errors.

    The assertion checks that Item.display() returns it's own id number.
    This isn't really testing anything, it's just a way to see if the
    information can be looked up without throwing an error. There is
    probably a better way to do this.
    """
    def test_item(self):

        for i in [1, 2, 6, 11, 15, 23, 24, 56, 57, 58, 59, 60, 61, 62, 63]:
            self.item = Item(i)
            result = self.item.display()
            self.assertEqual(result, i)


class RecipeTests(TestCase):
    """
    Same as the Item tests, a number of different recipes are displayed
    to check that there are no errors while getting the information
    from the API.
    """
    def test_recipe(self):
        test_nums = [1, 2, 3, 4, 5, 6, 7, 3454, 3455, 3456, 3457,
                     3458, 7497, 7498, 7499, 7500]

        for i in test_nums:
            self.recipe = Recipe(i)
            result = self.recipe.display()
            self.assertEqual(result, i)
