import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/eurlex/filtered.csv", sep=",", quotechar="'")

# print(df.columns)
# print(df['subject_matter'].value_counts()[df['subject_matter'].value_counts()>2006].index)
# print("\n")

print(df.groupby('subject_matter').filter(lambda x: len(x) == 3846).size().plot(kind='bar', rot=0))

# plt.show(block=True)