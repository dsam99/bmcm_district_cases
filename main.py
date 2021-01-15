import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter
import matplotlib as plt

import model
import data
import metric

def main():
    # https://www.ussc.gov/sites/default/files/pdf/research-and-publications/datafiles/USSC_Public_Release_Codebook_FY99_FY19.pdf
    # ^ the link above provides the number for each district. RI is 6
    district_num = 6 # make this RI and one other
    timeframe = [] # yearly updates to distributions

    df = pd.read_csv("justfair_dataset.csv")

    # features of importance & bin values
    features = ["FILEDATE", "DISPDATE", "MONSEX", "NEWRACE", "AGE", "CITIZEN",
                "NEWEDUC","XFOLSOR", "CRIMPTS", "FCOUNSEL"]
    ageframe=[15,30,50,65,80,150] # age buckets
    crimframe=[-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,25,1000] # CRIMPTS buckets

    df = df[df["CIRCDIST"] == district_num] # filter by district
    judge_names = set(df["judges"])
    judges = [model.Judge(name) for name in judge_names] # initialize judges

    df = df[features] # keep only the relevant features for our model
    df["FILEDATE"] = pd.to_datetime(df["FILEDATE"], format='%m/%d/%Y') # convert to datetimes
    df["DISPDATE"] = pd.to_datetime(df["DISPDATE"], format='%m/%d/%Y') # convert to datetimes
    df.dropna(inplace=True) # drop rows with missing values
    df["AGE"] = pd.cut(df["AGE"], ageframe) # bucket AGE based on ageframe
    df["CRIMPTS"] = pd.cut(df["CRIMPTS"],crimframe) # bucket CRIMPTS based on crimfame
    df.rename(columns={"MONSEX": "sex", "NEWRACE": "race", "AGE": "age",
                    "CITIZEN": "is_citizen", "NEWEDUC": "educ", "XFOLSOR": "crime",
                    "CRIMPTS": "crim_hist", "FCOUNSEL": "counsel"},inplace=True) # rename columns

	train_df, test_df = train_test_split(df, test_size=0.5) # half and half
    queue_model = model.District(timeframe) # initialize district model
    # x = datetime.datetime(2020, 1, 1)
    dfs = [] # stores separate DataFrame for each year
    for year in range(2000, 2010):
        # filter by year and sort by FILEDATE in ascending order
        dfs.append(train_df[train_df["FILEDATE"].year == year].sort_values("FILEDATE",inplace=true))

    for year_df in dfs:
        for idx, case in year_df.iterrows(): # assign the year's cases
            queue_model.process_case(case)

        global_dist = queue_model.global
        judge_dists = {j.name: j.dist for j in judges}

        # compute yearly metric
        val = metric.tv_metric(judge_dists, global_dist)
        workload_val = metric.workload_metric(judge_dists)



if __name__ == "__main__":
    main()
