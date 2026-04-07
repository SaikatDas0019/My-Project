import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(r"amazon.csv.zip")

data.columns = data.columns.str.upper()
data["RATING"] = data["RATING"].replace("|", 0)
data["RATING_COUNT"] = data["RATING_COUNT"].replace("|", 0)
data["RATING_COUNT"] = data["RATING_COUNT"].str.replace(",", "")
data["RATING"].astype(float)
data["RATING_COUNT"].astype(float)

rating = data["RATING"]
rating_count = data["RATING_COUNT"]

plt.plot(rating, marker='o', label="RATING")
plt.plot(rating_count, marker='o', label="RATING_COUNT")
plt.legend()
plt.title("Rating")
plt.show()