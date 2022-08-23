from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from http import HTTPStatus
import json
from api.models import Users
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def get(_, id):
    try:
        user = Users.objects.get(id=id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse({"id": str(user.id), "name": user.name})


@csrf_exempt
@require_http_methods(["POST"])
def post(request):
    body = json.loads(request.body)
    name = body.get('name')
    if name is None:
        return JsonResponse({'error': 'Invalid input'}, status=HTTPStatus.BAD_REQUEST)
    user = Users.objects.create(name=name)
    user_id = str(user.id)
    return JsonResponse({'success': 'User created %s'%(user_id)})
