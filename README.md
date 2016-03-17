# Guild Wars Calculator

## Description
Time to play with a real world api to produce something useful for the players. The end result of this program will calculate values and price differences for the Guild Wars 2 system. 

## Objectives

After completing this assignment you should be able to:
* Intepret API documentation
* Use multiple api calls with the `requests` library
* Convert json reponses to dictionaries/objects


### Normal Mode
Use the documentation found on the [Wiki](https://wiki.guildwars2.com/wiki/API:2).

Create a cli menu to select the following options:
* Recipe
* Item

After display the detail page for a recipe or item give the user the option to return to the main menu or quit.

Using `@staticmethod` and class objects change the JSON data into objects.  Minimum required are Item and Recipe. 

#### Recipe
For the recipe option take an id number and return the recipe with the following information:
* id
* type
* Output Item (Some of the below will require a call to the `items` endpoint)
	* Output item count
	* Output item name
	* min_rating
	* rarity
	* vendor_price
	* Buy/Sell prices for orders (`prices` endpoint)
* Use the `ingredients` list to get the following for each ingredient with the `items` endpoint
	* Name
	* Rarity
	* Buy price (prices endpoint)
	* Total price (buy price x quantity required)
* Display the difference between the buy price of ingredients and sell price of the output item to show cost of crafting goods.


#### Item
For the item take the id number and return the item with the following:
* id
* description
* type
* rarity
* level
* vendor_value
* game_types
* restrictions
* details
* Use the `listings` endpoint to find all current orders and display the highest buy price and the lowest sell price
* Display the spread between the two price points showing potential trade run values

### Hard Mode 

#### Character Selection
* Get an account for the game and create 1-2 characters (it is free to play)
* Get an API key.  Application [here](https://wiki.guildwars2.com/wiki/API:API_key) Make sure to include `inventories` scope

* Add a characters option to the main menu
* The option should list the characters (name/race/profession displayed) for your api key using the `characters` endpoint 
* Allow the user to pick the character
* Give all main information for the character
* Display the value of the character by the following calculation
	* Get the vendor_value for each item from the character
	* Include both worn items and inventory items
	* Exclude any item that is bound_to character
	* Total value is the value of all equipment sold that an be sold

#### Caching
Many things such as item information, recipes and basic character information does not change much over the run time of the program.  Implement a simple caching system to store the non-changing information.

* Create a dictionary for each type of information
* Each time an api is called for the information it should be inserted into the dictionary
* Before each api call is made for data the cache should be checked
* Hint: These can probably be stored in the class itself and accessed via @classmethod but not required

### Nightmare Mode

Using the `exchange/coins` endpoint to convert all coins to gems then use the cost (USD) of gems to convert all prices to dollars.  Display this calculation for each and every coin displayed program wide.  Please cache the exchange api so that only 1 call is required then it is basic math moving forward.


