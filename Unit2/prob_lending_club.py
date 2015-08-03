import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

loansData = pd.read_csv("https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv")
loansData.dropna(inplace=True)

plt.figure()
loansData.boxplot(column="Amount.Requested")
plt.savefig("amt_req_box.png")
loansData.hist(column="Amount.Requested")
plt.savefig("amt_req_hist.png")
plt.figure()
stats.probplot(loansData["Amount.Requested"], dist="norm", plot=plt)
plt.savefig("amt_req_qq.png")

