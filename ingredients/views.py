from django.http import HttpResponse
import logging
import simplejson as json
from ingredients.ingredients_repository import get_allergen_data_for_ingredients
logger = logging.getLogger(__name__)


def response_encoder(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


def batch_get_ingredients(request):
    # TODO: add token validation to ensure request only comes from my app
    if request.method != 'POST':
        return HttpResponse(status=405)

    request_data_unicode = request.body.decode('utf-8')
    request_data: dict = json.loads(request_data_unicode)

    logger.info(f'Handling batch_get_ingredient request. {request_data}')

    allergen_data = get_allergen_data_for_ingredients(request_data['ingredient_queries'], request_data['num_results'])
    formatted_response_body = json.dumps(allergen_data, default=response_encoder)

    return HttpResponse(status=200, content=formatted_response_body, content_type='application/json')
