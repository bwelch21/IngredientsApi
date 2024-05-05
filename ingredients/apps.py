from django.apps import AppConfig
from ingredients.ingredients_repository import initialize_ingredients_db, initialize_ingredient_names_db


class IngredientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingredients'

    def ready(self):
        initialize_ingredients_db()
        initialize_ingredient_names_db()
