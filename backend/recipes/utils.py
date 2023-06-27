from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import IngredientsRecipe


def get_shopping_list(request):
    """
    Формирование списка покупок для выгрузки.
    """
    user = request.user
    if not user.shopping_cart.exists():
        return Response(status=HTTP_400_BAD_REQUEST)

    ingredients = IngredientsRecipe.objects.filter(
        recipe__shopping_cart__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))

    shopping_list = (
        f'Список покупок для: {user.get_full_name()}\n\n'
    )
    shopping_list += '\n'.join([
        f'- {ingredient["ingredient__name"]} '
        f'({ingredient["ingredient__measurement_unit"]})'
        f' - {ingredient["amount"]}'
        for ingredient in ingredients
    ])

    filename = f'{user.username}_shopping_list.txt'
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
