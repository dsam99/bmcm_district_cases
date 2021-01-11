import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter

def get_data(df, features, district):
	'''
	Function to clean and split data into train and test data
	'''

	district_df = df.loc[df['CIRCDIST'] == district]
	new_df = district_df[features].dropna()

	# convert to numpy and split
	train_df, test_df = train_test_split(new_df, test_size=0.5)
	return train_df, test_df

def compute_empirical(df, feature):
	'''
	Function to compute empirical distribution accross a given features
	'''

	col = df[feature]
	total = len(col)
	c = Counter(col)
	emp_dist = {}
	for i in c:
		emp_dist[i] = c[i] / total

	return emp_dist


def compute_global(train_df, features):
	'''
	Function to get an estimate of population distribution over features
	'''

	global_dist = {}

	for f in features:
		global_dist[f] = compute_empirical(train_df, features[0])
	
	return global_dist

if __name__ == "__main__":

	# read in dataframe
	df = pd.read_csv("justfair_dataset.csv")
	df.head()

	# extract district and specific features
	district = 1
	features = ["AGE"]
	train_df, test_df = get_data(df, features, district)

	global_dist = compute_global(train_df, features)

