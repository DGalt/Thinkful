import pandas as pd
from scipy import stats

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

data = data.splitlines()
data = [i.split(", ") for i in data]

column_names = data[0]
data_rows = data[1:]
df = pd.DataFrame(data_rows, columns=column_names)
df.Alcohol = df.Alcohol.astype(float)
df.Tobacco = df.Tobacco.astype(float)

alc_range = df.Alcohol.max() - df.Alcohol.min()
tob_range = df.Tobacco.max() - df.Tobacco.min()

print("The ranges for the Alcohol and Tobacco data are: "
      "{} and {} pounds.".format(alc_range, tob_range))
print("The mean values for the Alcohol and Tobacco data are: "
      "{:0.2f} and {:0.2f} pounds.".format(df.Alcohol.mean(), df.Tobacco.mean()))
print("The median values for the Alcohol and Tobacco data are: "
      "{} and {} pounds.".format(df.Alcohol.median(), df.Tobacco.median()))
print("The mode values for the Alcohol and Tobacco data are: "
      "{} and {} pounds.".format(stats.mode(df.Alcohol)[0][0],
                                stats.mode(df.Tobacco)[0][0]))
print("The variances for the Alcohol and Tobacco data are: "
      "{:0.4f} and {:0.4f} pounds^2.".format(df.Alcohol.var(), df.Tobacco.var()))
print("The standard deviations for the Alcohol and Tobacco data are: "
      "{:0.4f} and {:0.4f} pounds.".format(df.Alcohol.std(), df.Tobacco.std()))

