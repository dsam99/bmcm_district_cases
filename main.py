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

    # w['female'] = w['female'].map({'female': 1, 'male': 0})
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

    # del df["judge"] # drop judges

    attr_feats = ["sex", "race", "age", "is_citizen", "educ", "crime", "crim_hist", "counsel"]
    attr_df = df[attr_feats]

    # making attribute values unique and changing the values in the dataframe
    attr_subattrs = {}
    attributes = set()
    counter = 0
    for attr in attr_feats:
        mapping = {}
        attr_subattrs[attr] = []
        for val in attr_df[attr].unique():
            mapping[val] = counter
            attributes.add(counter)
            attr_subattrs[attr].append(counter)
            counter += 1
        attr_df[attr] = attr_df[attr].map(mapping)
        df[attr] = df[attr].map(mapping)

    # creating a set
    # attributes = set()
    # for _, row in attr_df.iterrows():
    #     for _, attr in row.iteritems():
    #         attributes.add(attr)

    #print(attributes)


    dfs = [] # stores separate DataFrame for each year
    for year in range(1990, 2018):
        # filter by year and sort by FILEDATE in ascending order
        dfs.append(df[df["FILEDATE"].dt.year == year].sort_values("FILEDATE"))

    def marginalize(attr):
        """
        Prints the marginals for each subattribute of attr
        """
        # find the keys associated with attr
        # then find their distributions from each judge
        subattrs = attr_subattrs[attr]
        for s in subattrs:
            print([j.dist[s] for j in judges])

    for year in range(1990,2018):
        year_df = dfs[year - 1990]
        print(year)
        judge_names = set(year_df["judge"])
        if len(judge_names) == 0:
            continue
        judges = [model.Judge(name, attributes, attr_feats) for name in judge_names] # initialize judges
        uniform_judges = [model.Judge(name, attributes, attr_feats) for name in judge_names] # initialize uniform
        actual_judges = [model.Judge(name, attributes, attr_feats) for name in judge_names] # initialize uniform

        for idx, case in year_df.iterrows(): # assign the year's cases
            model.process_case(attributes, case, judges)
            model.assign_uniformly(case, uniform_judges)
            model.assign_by_name(case, actual_judges)

        judge_dists = {j.name: j.dist for j in judges}
        uniform_judge_dists = {j.name: j.dist for j in uniform_judges}
        actual_judge_dists = {j.name: j.dist for j in actual_judges}

        # compute yearly metric
        val = metric.tv_metric(attributes, judge_dists)
        print("Model: " + str(val[0]))
        uniform_val = metric.tv_metric(attributes, uniform_judge_dists)
        print("Uniform: " + str(uniform_val[0]))
        actual_val = metric.tv_metric(attributes, actual_judge_dists)
        print("Actual: " + str(actual_val[0]))

        # statistical uniformity metric
        unif_val = metric.uniformity_metric(attributes,judge_dists)
        print("Unif Model: " + str(unif_val[0]))
        unif_uniform_val = metric.uniformity_metric(attributes, uniform_judge_dists)
        print("Unif Uniform: " + str(unif_uniform_val[0]))
        unif_actual_val = metric.uniformity_metric(attributes, actual_judge_dists)
        print("Unif Actual: " + str(unif_actual_val[0]))



        # workload_val = metric.workload_metric(judge_dists)
        print([(j.name,j.case_count) for j in judges])
        print([(j.name,j.case_count) for j in uniform_judges])
        print([(j.name,j.case_count) for j in actual_judges])
        # marginalize("sex")
        # marginalize("race")




if __name__ == "__main__":
    main()
