from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from http import HTTPStatus
from api.models import LoanOffers
from django.views.generic import ListView
from api.constants import DECLINATION_REASONS


class LoanOffersListHandler(ListView):
    model = LoanOffers

    def get_queryset(self):
        return self.model.objects.filter(user__id=self.kwargs.get('user_id'))
    
    def render_to_response(self, context):
        loan_offers = []
        for loan_offer in context.get('object_list'):
            loan_offers.append(self.serialize_loan_offer(loan_offer))
        return JsonResponse({"loan_offers": loan_offers})
    
    def serialize_loan_offer(self, loan_offer):
        return {
            "apr": round(loan_offer.apr/100, 2) if loan_offer.apr else None,
            "monthly_payments": loan_offer.monthly_payments,
            "term_length_months": loan_offer.term_length_months,
            "accept": loan_offer.accept,
            "reasons": [DECLINATION_REASONS.get(reason) for reason in loan_offer.reasons.split(",")] if loan_offer.reasons else None
        }
    

@require_http_methods(["GET"])
def get(_, user_id):
    try:
        loan_offers = LoanOffers.objects.filter(user__id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse({'loan_offers': loan_offers.values()})
