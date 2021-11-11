import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/eurlex/filtered.csv", sep=",", quotechar="'")

print(df.groupby('form').size().plot(kind='bar', rot=0))

plt.show(block=True)