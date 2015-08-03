import pandas as pd
from scipy import stats
import collections

# load data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#drop nulls
loansData.dropna(inplace=True)

#find frequency of unique values
freq = collections.Counter(loansData["Open.CREDIT.Lines"])

#calculate chi square and print result
chi, p = stats.chisquare(freq.values())

print("Chi-squared value of {} with a p value of {}".format(chi, p))

