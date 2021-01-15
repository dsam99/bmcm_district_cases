import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter
import matplotlib as plt
import sys

import model
import data
import metric

def main():
    # https://www.ussc.gov/sites/default/files/pdf/research-and-publications/datafiles/USSC_Public_Release_Codebook_FY99_FY19.pdf
    # ^ the link above provides the number for each district. RI is 6
    district_num = 68 # make this RI and one other
    timeframe = [] # yearly updates to distributions

    # features of importance & bin values
    features = ["FILEDATE", "DISPDATE", "MONSEX", "NEWRACE", "AGE", "CITIZEN",
                "NEWEDUC","XFOLSOR", "CRIMPTS", "FCOUNSEL", "judge"]

    ageframe=[15,30,50,65,80,150] # age buckets
    crimframe=[-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,25,1000] # CRIMPTS buckets

    # create df
    # data.process_df(district_num, features, ageframe, crimframe, "dist_68.csv")
    # sys.exit()

    # read DataFrame
    df = pd.read_csv("dist_68.csv")
    df["FILEDATE"] = pd.to_datetime(df["FILEDATE"], format='%m/%d/%Y') # convert to datetimes
    df["DISPDATE"] = pd.to_datetime(df["DISPDATE"], format='%m/%d/%Y') # convert to datetimes
    judge_names = set(df["judge"])
    del df["judge"] # drop judges

    attr_feats = ["sex", "race", "age", "is_citizen", "educ", "crime", "crim_hist", "counsel"]
    attr_df = df[attr_feats]

    # creating a set
    attributes = set()
    for _, row in attr_df.iterrows():
        for _, attr in row.iteritems():
            attributes.add(attr)

    judges = [model.Judge(name, attributes, attr_feats) for name in judge_names] # initialize judges
    dfs = [] # stores separate DataFrame for each year
    for year in range(2000, 2010):
        # filter by year and sort by FILEDATE in ascending order
        dfs.append(df[df["FILEDATE"].dt.year == year].sort_values("FILEDATE"))

    for year_df in dfs:
        for idx, case in year_df.iterrows(): # assign the year's cases
            model.process_case(attributes, case, judges)

        judge_dists = {j.name: j.dist for j in judges}

        # compute yearly metric
        val = metric.tv_metric(attributes, judge_dists)
        print(val[0])
        # workload_val = metric.workload_metric(judge_dists)

if __name__ == "__main__":
    main()
