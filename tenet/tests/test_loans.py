from django.test import Client, TestCase
from api.models import Users, LoanApplications, LoanOffers
from api.constants import LOW_CREDIT_SCORE, BANKRUPTCY, DELINQUENCY, DEBT_TO_INCOME, LOAN_TO_VALUE



class TestEndpointBase(TestCase):
    
    def setUp(self):
        self.user = Users.objects.create(name="John Doe")
        self.user_id = str(self.user.id)
        self.client = Client()
        self.expected_loan_app_details = {
            "user_id": self.user.id,
            "credit_score": 700,
            "monthly_debt": 100034,
            "monthly_income": 1133358,
            "bankruptcies": 0,
            "delinquencies": 0,
            "vehicle_value": 2034334,
            "loan_amount": 1693467
        }


class TestPostLoanApplicationsEndpoint(TestEndpointBase):
    
    endpoint = '/api/users/%s/loan-applications/'

    def setUp(self):
        self.user = Users.objects.create(name="John Doe")
        self.user_id = str(self.user.id)
        self.client = Client()
        self.expected_loan_app_details = {
            "user_id": self.user.id,
            "credit_score": 700,
            "monthly_debt": 100034,
            "monthly_income": 1133358,
            "bankruptcies": 0,
            "delinquencies": 0,
            "vehicle_value": 2034334,
            "loan_amount": 1693467
        }

    def test_create_loan_application(self):
        response = self.client.post(self.endpoint%(self.user_id), data=self.expected_loan_app_details, content_type="application/json")
        loan_application = LoanApplications.objects.get(user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.expected_loan_app_details.pop('user_id'), loan_application.user.id)
        for key, expected_loan_app_detail in self.expected_loan_app_details.items():
            self.assertEqual(getattr(loan_application, key), expected_loan_app_detail)


class TestLoanOfferEndponit(TestEndpointBase):
    
    endpoint = '/api/users/%s/loan-applications/'

    def setUp(self):
        self.user = Users.objects.create(name="John Doe")
        self.user_id = str(self.user.id)
        self.client = Client()
        self.expected_loan_app_details = {
            "user_id": self.user.id,
            "credit_score": 700,
            "monthly_debt": 100034,
            "monthly_income": 1133358,
            "bankruptcies": 0,
            "delinquencies": 0,
            "vehicle_value": 2034334,
            "loan_amount": 1693467
        }

    def test_offer_declined_for_low_credit_score(self):
        self.expected_loan_app_details["credit_score"] = 650
        response = self.client.post(self.endpoint%(self.user_id), data=self.expected_loan_app_details, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        loan_offer = LoanOffers.objects.get(user=self.user)
        self.assertEqual(loan_offer.reasons, LOW_CREDIT_SCORE)
        for attr in ['apr', 'monthly_payments', 'term_length_months', 'accept']:    
            self.assertIsNone(getattr(loan_offer, attr))

    def test_offer_declined_for_bankruptcy(self):
        self.expected_loan_app_details["bankruptcies"] = 1
        response = self.client.post(self.endpoint%(self.user_id), data=self.expected_loan_app_details, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        loan_offer = LoanOffers.objects.get(user=self.user)
        self.assertEqual(loan_offer.reasons, BANKRUPTCY)
        for attr in ['apr', 'monthly_payments', 'term_length_months', 'accept']:    
            self.assertIsNone(getattr(loan_offer, attr))
    
    def test_offer_declined_for_delinquencies(self):
        self.expected_loan_app_details["delinquencies"] = 1
        response = self.client.post(self.endpoint%(self.user_id), data=self.expected_loan_app_details, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        loan_offer = LoanOffers.objects.get(user=self.user)
        self.assertEqual(loan_offer.reasons, DELINQUENCY)
        for attr in ['apr', 'monthly_payments', 'term_length_months', 'accept']:    
            self.assertIsNone(getattr(loan_offer, attr))

    def test_offer_declined_for_debt_to_income(self):
        self.expected_loan_app_details["monthly_debt"] = 61
        self.expected_loan_app_details["monthly_income"] = 100
        response = self.client.post(self.endpoint%(self.user_id), data=self.expected_loan_app_details, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        loan_offer = LoanOffers.objects.get(user=self.user)
        self.assertEqual(loan_offer.reasons, DEBT_TO_INCOME)
        for attr in ['apr', 'monthly_payments', 'term_length_months', 'accept']:    
            self.assertIsNone(getattr(loan_offer, attr))
    
    def test_offer_declined_for_ltv(self):
        self.expected_loan_app_details["loan_amount"] = 20000
        self.expected_loan_app_details["vehicle_value"] = 10000
        response = self.client.post(self.endpoint%(self.user_id), data=self.expected_loan_app_details, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        loan_offer = LoanOffers.objects.get(user=self.user)
        self.assertEqual(loan_offer.reasons, LOAN_TO_VALUE)
        for attr in ['apr', 'monthly_payments', 'term_length_months', 'accept']:    
            self.assertIsNone(getattr(loan_offer, attr))
    
    def test_offer_declined_for_multiple_reasons(self):
        self.expected_loan_app_details["monthly_debt"] = 61
        self.expected_loan_app_details["monthly_income"] = 100
        self.expected_loan_app_details["loan_amount"] = 20000
        self.expected_loan_app_details["vehicle_value"] = 10000
        response = self.client.post(self.endpoint%(self.user_id), data=self.expected_loan_app_details, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        loan_offer = LoanOffers.objects.get(user=self.user)
        self.assertEqual(loan_offer.reasons, DEBT_TO_INCOME+","+LOAN_TO_VALUE)
        for attr in ['apr', 'monthly_payments', 'term_length_months', 'accept']:    
            self.assertIsNone(getattr(loan_offer, attr))


class TestLoanOffersEndPoint(TestEndpointBase):
    endpoint = '/api/users/%s/loan-offers/'

    def test_get_loan_offer(self):
        self.expected_loan_app_details.pop("user_id")
        LoanApplications.objects.create(user=self.user, **self.expected_loan_app_details)
        response = self.client.get(self.endpoint%(self.user_id))
        self.assertEqual(response.status_code, 200)
