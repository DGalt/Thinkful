import pandas as pd
import statsmodels.api as sm
import math

df = pd.read_csv("loansData_clean.csv")
#df["Interest.Rate"] *= 100
df["IR_TF"] = df["Interest.Rate"] <= .12

#print df["IR_TF"].head(5), df["Interest.Rate"].head(5)

#if use what's in curriculum, get empty dataframe. Interest.Rate is represented
#as decimals (0.1 = 10%, etc), so maybe that's why
#this works if that is the case: 
#print df["IR_TF"][df["Interest.Rate"] == .10].head()
#this is still returning empty dataframe though:
#print df[df["Interest.Rate"] == .13].head()

df["Intercept"] = 1.0

#not sure what the independent variables are for this assignment 
ind_vars = ["FICO.Score", "Amount.Requested", "Intercept"]

#define logistic regression model
logit = sm.Logit(df["IR_TF"], df[ind_vars])

#fit the model
result = logit.fit()

#get fitted coefficients
coeff = result.params
print coeff

FicoScore = 720
AmountRequested = 10000
Intercept = coeff["Intercept"]

interest_rate = (Intercept + coeff["FICO.Score"]*FicoScore
                 + coeff["Amount.Requested"]*AmountRequested)
print "Interest rate: {}".format(interest_rate)

p = 1/(1 + math.exp(Intercept + coeff["FICO.Score"]*FicoScore
                    + coeff["Amount.Requested"]*AmountRequested))
print "Probability: {}".format(p)

def logistic_function(FICO_score, LoanAmount, coeff=coeff):
    """Function to calculate  p - probability - of receiving a loan of 
    LoanAmount given a certain FICO_score."""
    Fico_coef = coeff["FICO.Score"]
    Amt_coef = coeff["Amount.Requested"]
    Intercept = coeff["Intercept"]

    return 1/(1 + math.exp(Intercept + Fico_coef*FICO_score
                           + Amt_coef*LoanAmount))

print("Probability of getting a $10000 loan at <= 12% interest with a FICO "
      "score of 720 is: {:0.2}".format(logistic_function(720, 10000)))

def pred(FICO_score, LoanAmount, threshold=0.7, coeff=coeff):
    """Function to determine whether individual will receive a loan given 
    a certain request amount and that individual's FICO score"""
    Fico_coef = coeff["FICO.Score"]
    Amt_coef = coeff["Amount.Requested"]
    Intercept = coeff["Intercept"]

    p = 1/(1 + math.exp(Intercept + Fico_coef*FICO_score
                           + Amt_coef*LoanAmount))

    if p >= threshold:
        return "You will get the loan"
    else:
        return "You will not get the loan"

print pred(720, 10000)
print pred(400, 10000)





