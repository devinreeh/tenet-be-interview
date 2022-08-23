from django.db import models
import numpy_financial as npf
import uuid


class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)


class LoanApplications(models.Model):
    user = models.ForeignKey('Users', related_name='loans', on_delete=models.CASCADE)
    loan_offer = models.OneToOneField('LoanOffers', related_name='loan_application', null=True, blank=True, on_delete=models.CASCADE)
    credit_score = models.PositiveSmallIntegerField()
    monthly_debt = models.PositiveIntegerField()
    monthly_income = models.PositiveIntegerField()
    bankruptcies = models.PositiveSmallIntegerField()
    delinquencies = models.PositiveSmallIntegerField()
    vehicle_value = models.PositiveIntegerField()
    loan_amount = models.PositiveIntegerField()


    @property
    def apr(self):
        if self.credit_score >= 780:
            return 2
        elif 720 <= self.credit_score and self.credit_score < 780:
            return 5
        elif 660 <= self.credit_score and self.credit_score < 719:
            return 8
        else:
            return 0
    
    def calculate_monthly_payment(self, apr=None):
        apr = self.apr if not apr else apr
        monthly_payment = npf.pmt(apr/12/100, 72, self.loan_amount/100)
        return -monthly_payment


class LoanOffers(models.Model):
    user = models.ForeignKey('Users', related_name='loan_offers', on_delete=models.CASCADE)
    apr = models.PositiveIntegerField(null=True, blank=True)
    monthly_payments = models.PositiveIntegerField(null=True, blank=True)
    term_length_months = models.PositiveSmallIntegerField(null=True, blank=True)
    accept = models.BooleanField(null=True, blank=True)
    reasons = models.CharField(max_length=200, null=True, default=None, blank=True)
