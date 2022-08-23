from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import LoanApplications, LoanOffers
from api.constants import LOW_CREDIT_SCORE, BANKRUPTCY, DELINQUENCY, DEBT_TO_INCOME, LOAN_TO_VALUE
from decimal import Decimal


@receiver(post_save, sender=LoanApplications)
def create_loan_offer(sender, instance, created, **kwargs):
    if not created:
        return
    
    reasons = []
    
    apr = instance.apr
    if apr == 0:
        reasons.append(LOW_CREDIT_SCORE)
    else:
        monthly_payment_new_loan = instance.calculate_monthly_payment(apr=apr)
        debt_to_income = (instance.monthly_debt + monthly_payment_new_loan)/instance.monthly_income*100
        if debt_to_income > 60:
            reasons.append(DEBT_TO_INCOME)

    if instance.bankruptcies > 0:
        reasons.append(BANKRUPTCY)
    if instance.delinquencies > 0:
        reasons.append(DELINQUENCY)
    if instance.vehicle_value < instance.loan_amount:
        reasons.append(LOAN_TO_VALUE)

    if reasons:
        LoanOffers.objects.create(user=instance.user, reasons=",".join(reasons))
    else:
        monthly_payment_new_loan = round(monthly_payment_new_loan, 2)*100
        LoanOffers.objects.create(user=instance.user, apr=apr, monthly_payments=monthly_payment_new_loan, term_length_months=72)
