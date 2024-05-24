import csv
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from langchain.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

csv_data = None
vector_db = None

ingredient_dict = {}


@dataclass
class IngredientLookupResult:
    ingredient_name: str
    score: float


def initialize_ingredient_names_db():
    global vector_db
    global csv_data
    if csv_data is None:
        loader = CSVLoader(file_path='ingredients/data/ingredient_names.csv')
        csv_data = loader.load()

        texts = [doc.page_content for doc in csv_data]

        embeddings = OpenAIEmbeddings()
        embeddings.embed_documents(texts)

        vector_db = FAISS.from_documents(csv_data, embeddings)

        return vector_db


def initialize_ingredients_db():
    global ingredient_dict
    with (open('ingredients/data/ingredients.csv', 'r') as file):
        reader = csv.reader(file)
        for row in reader:
            ingredient_name = row[0]
            detailed_ingredient = {
                'name': ingredient_name,
                'category': row[1],
                'description': row[2],
                'allergen_profile': {
                    '321705f7d2784acd9e8b44b8436b9356': {
                        'allergen': {
                            'id': '321705f7d2784acd9e8b44b8436b9356',
                            'name': 'Egg'
                        },
                        'rating': row[3],
                        'note': row[4],
                    },
                    'fcfbe6ec79814143879b1e2ea1e4fd8c': {
                        'allergen': {
                            'id': 'fcfbe6ec79814143879b1e2ea1e4fd8c',
                            'name': 'Fish'
                        },
                        'rating': row[5],
                        'note': row[6],
                    },
                    '9395ac9233ad4fffa2181a54ea81e34f': {
                        'allergen': {
                            'id': '9395ac9233ad4fffa2181a54ea81e34f',
                            'name': 'Milk'
                        },
                        'rating': row[7],
                        'note': row[8],
                    },
                    'b96a2283396647bb8447afde85272a40': {
                        'allergen': {
                            'id': 'b96a2283396647bb8447afde85272a40',
                            'name': 'Peanut'
                        },
                        'rating': row[9],
                        'note': row[10],
                    },
                    'f683bf47615946b9b5d7842eb84db274': {
                        'allergen': {
                            'id': 'f683bf47615946b9b5d7842eb84db274',
                            'name': 'Sesame'
                        },
                        'rating': row[11],
                        'note': row[12],
                    },
                    '881bd111a0d54f39b51173a7389ce454': {
                        'allergen': {
                            'id': '881bd111a0d54f39b51173a7389ce454',
                            'name': 'Shellfish'
                        },
                        'rating': row[13],
                        'note': row[14],
                    },
                    'd76ed8a6ecaa4b8db0f750681bec57f1': {
                        'allergen': {
                            'id': 'd76ed8a6ecaa4b8db0f750681bec57f1',
                            'name': 'Soy'
                        },
                        'rating': row[15],
                        'note': row[16],
                    },
                    '633ee1fe98c04fb9a45438dfd4c86cb9': {
                        'allergen': {
                            'id': '633ee1fe98c04fb9a45438dfd4c86cb9',
                            'name': 'Tree nut'
                        },
                        'rating': row[17],
                        'note': row[18],
                    },
                    '81c56e3f96b14b8a92841c3db54a3cd2': {
                        'allergen': {
                            'id': '81c56e3f96b14b8a92841c3db54a3cd2',
                            'name': 'Wheat'
                        },
                        'rating': row[19],
                        'note': row[20],
                    },
                },
            }

            ingredient_dict[ingredient_name] = detailed_ingredient

    return ingredient_dict


def get_ingredient_db():
    if vector_db is None:
        raise Exception('Ingredients DB is not initialized.')
    return vector_db


def get_allergen_data_for_ingredients(ingredient_queries, num_results):

    # Parallelize the lookup_ingredient() calls using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        lookup_futures = [executor.submit(lookup_detailed_ingredient, query, num_results) for query in ingredient_queries]
        query_results = [future.result() for future in lookup_futures]

    return dict(zip(ingredient_queries, query_results))


def lookup_detailed_ingredient(ingredient_query, num_results=3):
    # Get the most similar ingredient from the database.
    # TODO: There's a strange issue with the similarity search where the results are not consistent.
    #  Sometimes the same query will return different results. Investigate ways to improve consistency:
    #  https://www.perplexity.ai/search/I-have-a-nhzQcn67QmS7dsHh6IK_7g#0
    search_results = get_ingredient_db().similarity_search_with_score(query=ingredient_query, k=num_results)
    ingredient_lookup_results = [
        get_detailed_ingredient(IngredientLookupResult(extract_ingredient_name(result), float(score))) for result, score in search_results
    ]

    return ingredient_lookup_results


def get_detailed_ingredient(similar_term: IngredientLookupResult):
    detailed_ingredient = ingredient_dict[similar_term.ingredient_name]
    detailed_ingredient['relevancy_score'] = similar_term.score
    return detailed_ingredient


def extract_ingredient_name(result):
    return result.page_content.replace('Name: ', '')
