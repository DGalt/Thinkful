xbimport pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData["Interest.Rate"] = map(lambda x: float(x.strip("%"))/100, loansData['Interest.Rate'])
loansData["Loan.Length"] = map(lambda x: float(x.strip(" months")), loansData["Loan.Length"])
loansData["FICO.Score"] = map(lambda x: float(x.split("-")[0]), loansData["FICO.Range"])

                               
#print loansData['Interest.Rate'].head(5)
#print loansData['Loan.Length'].head(5)
#print loansData['FICO.Score'].head(5)

#plt.figure()
#p = loansData['FICO.Score'].hist()
#a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10))
#a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
#plt.show()

#Linear model for Interst rate:
#InterestRate = b + a1(FICO.Score) + a2(Loan.Amount)

intrate = loansData["Interest.Rate"]
loanamt = loansData["Amount.Requested"]
fico = loansData["FICO.Score"]

#The dependent variable - need to reshape (why)
y = np.matrix(intrate).transpose()
#The indepent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

#put two columsn together to form an input matrix
x = np.column_stack([x1, x2])

#create linear model
X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()

#results summary:
print f.summary()
