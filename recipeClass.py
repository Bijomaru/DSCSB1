
import requests
from utilities import utilities 


class Recipes:
    """
    A class used to get recipes from spoonocular and their steps
    
    """
    def recipesList(diet, number):
        """
        A method to search the recipes on spoonocular

        Parameters
        ----------
        diet is one of the diets in the list from soppocular 
        https://spoonacular.com/food-api/docs#Diets
        
        number is the number of recipes to show in the results

        TODO test the value given in diet to fit the possible values
        TODO test the value in number to be always a string
        TODO implement other searchs parameters

        """
        
        response = requests.get('https://api.spoonacular.com/recipes/complexSearch?apiKey='
                                + utilities.spoonKey 
                                + '&query=' 
                                + '&diet=' + diet 
                                + "&number=" + str(number)
                                )
        # print(response.json())
        return response.json()['results']




    def recipeIngredients(recipeID):
        """
        Method to get a list of ingredient based on the ID of the recipe

        Parameters
        ----------
        recipeID is the ID that indentify the recipe, this ID should be input by the user
        """
        response = requests.get('https://api.spoonacular.com/recipes/'
                                +str(recipeID) 
                                +'/ingredientWidget.json'
                                +'?apiKey=' + utilities.spoonKey
                                )
        return response.json()['ingredients']

    
    def allRecipeSteps(recipeID):
        """
        Method to get all the recipes steps

        Parameters
        ----------
        recipeID ID that indentify the recipe
        """
        response= requests.get('https://api.spoonacular.com/recipes/'
        + str(recipeID)
        +'/analyzedInstructions'
        +'?apiKey=' + utilities.spoonKey
        )
        return response.json()[0]['steps']


