from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from http import HTTPStatus
import json
from api.models import LoanApplications, Users
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class LoanApplicationsHandler(View):

    def get(self, _, id):
        try:
            user = LoanApplications.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=HTTPStatus.NOT_FOUND)
        return JsonResponse({"id": user.id, "name": user.name})

    def post(self, request, user_id):
        body = json.loads(request.body)
        user = Users.objects.get(id=user_id)
        credit_score = body.get('credit_score')
        monthly_debt = body.get('monthly_debt')
        monthly_income = body.get('monthly_income')
        bankruptcies = body.get('bankruptcies')
        delinquencies = body.get('delinquencies')
        vehicle_value = body.get('vehicle_value')
        loan_amount = body.get('loan_amount')
        LoanApplications.objects.create(user=user,
                                        credit_score=credit_score,
                                        monthly_debt=monthly_debt,
                                        monthly_income=monthly_income,
                                        bankruptcies=bankruptcies,
                                        delinquencies=delinquencies,
                                        vehicle_value=vehicle_value,
                                        loan_amount=loan_amount)
        return JsonResponse({'success': 'Created loan application'})
