import matplotlib.pyplot as plt
import scipy.stats as stats
import collections

#not sure if this is the correct data to be using
#"data in this less" from Challenge is not clear
data = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6,
        6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

c = collections.Counter(data)

for j, k in c.items():
    print("{} occurs {} time(s)".format(j, k))

boxplot = plt.boxplot(data)
plt.savefig("prob_dist_boxplot.png")
plt.figure()
hist = plt.hist(data)
plt.savefig("prob_dist_histogram.png")
plt.figure()
qq_plot = stats.probplot(data, dist="norm", plot=plt)
plt.savefig("prob_dist_qq.png")
