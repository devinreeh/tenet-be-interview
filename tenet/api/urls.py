from django.urls import path
from api.handlers import users, loan_applications, loan_offers

urlpatterns = [
    path('users/', users.post, name='post-users'),
    path('users/<uuid:id>/', users.get, name='get-users'),
    path('users/<uuid:user_id>/loan-applications/', loan_applications.LoanApplicationsHandler.as_view(), name='loan-applications'),
    path('users/<uuid:user_id>/loan-offers/', loan_offers.LoanOffersListHandler.as_view(), name='loan-offers'),
]
