import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

#load data - first row is some annotation info, so have to skip it
loansData = pd.read_csv('LoanStats3c.csv', skiprows=[0])

#remove rows with na - should I be doing this? 
loansData.dropna(inplace=True)

# print loansData["annual_inc"].head()
# print loansData["int_rate"].head()
# print loansData["home_ownership"].head()

#convert int_rate into numeric value
loansData["int_rate"] = [float(x.strip("%"))/100
                         for x in loansData["int_rate"]]
#print loansData["int_rate"].head()

################################################################################
# Model interest rates as a function of income
################################################################################
y = np.matrix(loansData["int_rate"]).transpose()
x1 = np.matrix(loansData["annual_inc"]).transpose()

X = sm.add_constant(x1)
model = sm.OLS(y, X)
f = model.fit()

print f.summary()
#plt.scatter(x1, y)
#plt.show()

################################################################################
# Add home ownership to the model
################################################################################

#gives counts of different values - want to see what possible values are in
#the home_ownership category
#print loansData["home_ownership"].value_counts()

# for x, y in zip(loansData["home_ownership"][0:20].values,
#                 pd.Categorical(loansData["home_ownership"]).codes[0:20]):
#     print x, y

#convert categorical home ownership values to numeric values
loansData["home_own_num"] = pd.Categorical(loansData["home_ownership"]).codes
#print loansData["home_own_num"].head()

x2 = np.matrix(loansData["home_own_num"]).transpose()

x = np.column_stack([x1, x2])

X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()

print f.summary()
# plt.scatter(x2, y)
# plt.show()

## Try using formulaic interface
est = smf.ols(formula = 'int_rate ~ annual_inc + home_own_num',
              data=loansData).fit()
print est.summary()

##look at interaction
est = smf.ols(formula = 'int_rate ~ annual_inc * home_own_num',
              data=loansData).fit()
print est.summary()
