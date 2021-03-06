import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter

def process_df(district_num, features, ageframe, crimframe, filename):

	df = pd.read_csv("justfair_dataset.csv")
	df = df[df["CIRCDIST"] == district_num] # filter by district

	df = df[features] # keep only the relevant features for our model
	# df["FILEDATE"] = pd.to_datetime(df["FILEDATE"], format='%m/%d/%Y') # convert to datetimes
	# df["DISPDATE"] = pd.to_datetime(df["DISPDATE"], format='%m/%d/%Y') # convert to datetimes
	df.dropna(inplace=True) # drop rows with missing values
	df["AGE"] = pd.cut(df["AGE"], ageframe) # bucket AGE based on ageframe
	df["CRIMPTS"] = pd.cut(df["CRIMPTS"],crimframe) # bucket CRIMPTS based on crimfame
	df.rename(columns={"MONSEX": "sex", "NEWRACE": "race", "AGE": "age",
					"CITIZEN": "is_citizen", "NEWEDUC": "educ", "XFOLSOR": "crime",
					"CRIMPTS": "crim_hist", "FCOUNSEL": "counsel"},inplace=True) # rename columns

	# save dataframe
	df.to_csv(filename) # keep this line for main.py, remove for main2.py
	return df


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

def compute_judges(train_df, judges, features):
	'''
	Function to compute the estimate of judge distribution over features
	'''

	judge_counts = {}



	for index, j in enumerate(judges):

		if j not in judge_counts:
			judge_counts[j] = {f:{} for f in features}
		for i, f in enumerate(features):
			val = train_df[f].values[index]
			print(val)
			if val in judge_counts[j][f]:
				judge_counts[j][f][val] += 1
			else:
				judge_counts[j][f][val] = 1

	return judge_counts

if __name__ == "__main__":

	# read in dataframe
	df = pd.read_csv("justfair_dataset.csv")
	df.head()

	# extract district and specific features
	district = 1
	features = ["AGE", "judge"]
	train_df, test_df = get_data(df, features, district)

	# extract judge names
	judge_names_train = train_df["judge"]
	judge_names_test = test_df["judge"]

	# dropping judges
	del train_df["judge"]
	del test_df["judge"]

	global_dist = compute_global(train_df, features)

	# compute judge distribution
	features.remove("judge")
	judge_dist = compute_judges(train_df, judge_names_train, features)
	print(judge_dist)
