# Tenet BE Interview

## Demo:
To get dockerized api up and running
```
docker-compose build
```
```
docker-compose run tenet python tenet/manage.py migrate
```
```
docker-compose up
```

### Create User with POST
```
curl -d '{"name":"John Doe"}' -H 'Content-Type: application/json' POST http://0.0.0.0:8000/api/users/
```

### Retrieve User with GET
```
curl http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/
```

### Create Loan Application that Will Be Approved
```
curl -d '{"credit_score": 700, "monthly_debt": 100034, "monthly_income": 1133358, "bankruptcies": 0, "delinquencies": 0, "vehicle_value": 2034334, "loan_amount": 1693467}' -H 'Content-Type: application/json' POST http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/loan-applications/
```

### Create Loan Application that Will Be Declined for Low Credit Score
```
curl -d '{"credit_score": 640, "monthly_debt": 100034, "monthly_income": 1133358, "bankruptcies": 0, "delinquencies": 0, "vehicle_value": 2034334, "loan_amount": 1693467}' -H 'Content-Type: application/json' POST http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/loan-applications/
```

### Create Loan Application that Will Be Declined for Bankruptcy
```
curl -d '{"credit_score": 700, "monthly_debt": 100034, "monthly_income": 1133358, "bankruptcies": 1, "delinquencies": 0, "vehicle_value": 2034334, "loan_amount": 1693467}' -H 'Content-Type: application/json' POST http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/loan-applications/
```
### Create Loan Application that Will Be Declined for Delinquency
```
curl -d '{"credit_score": 700, "monthly_debt": 100034, "monthly_income": 1133358, "bankruptcies": 0, "delinquencies": 2, "vehicle_value": 2034334, "loan_amount": 1693467}' -H 'Content-Type: application/json' POST http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/loan-applications/
```

### Create Loan Application that Will Be Declined for Invalid Debt to Income Ratio
```
curl -d '{"credit_score": 700, "monthly_debt": 100034, "monthly_income": 1133358, "bankruptcies": 0, "delinquencies": 0, "vehicle_value": 2034334, "loan_amount": 1693467}' -H 'Content-Type: application/json' POST http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/loan-applications/
```
### Create Loan Application that Will Be Declined for Invalid Loan to Value Ratio
```
curl -d '{"credit_score": 700, "monthly_debt": 100034, "monthly_income": 1133358, "bankruptcies": 0, "delinquencies": 0, "vehicle_value": 1000000, "loan_amount": 1693467}' -H 'Content-Type: application/json' POST http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/loan-applications/
```

### Retrieve Loan Offer
```
curl http://0.0.0.0:8000/api/users/16ac6557-dfe7-4e06-97d5-379adb0a1a9b/loan-offers/
```
---

## Design Decisions:

1. Used integers for loan percentages and currency related fields because doing math with floating points can often result in rounding errors
2. Used three tables and added user relationships to Loan Offers and Loan Application tables because from the user's point of view they'll have access to only their own loan offers and applications
---

## Things to spend more time on:

1. Authentication
2. Authorization
3. Request Sanitization
4. Adding some way to just get formmatted values vs values for computation
5. Beter unit tests
6. More thought in into utility functions and modularization
7. Smaller commits
8. Docker environment configuration
9. Django settings
10. Specify versions for all dependencies

Time to complete demo about 3.25 hrs not including setting up github repo.
