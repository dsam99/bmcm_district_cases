import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.stats as ss
from collections import defaultdict

# mean judge assumption

class Judge:
    def __init__(self, name):
        self.name = name
        self.dist = {"sex": defaultdict(int), "race": defaultdict(int), "age": defaultdict(int),
                     "is_citizen": defaultdict(int), "educ": defaultdict(int),
                     "crime": defaultdict(int), "crim_hist": defaultdict(int), "counsel": defaultdict(int)}
        self.cases = [] # queue

        def add_case(case):
            '''
            Function to add a case to the queue and update distribution
            '''
            self.cases.append(case)
            for a in self.dist:
                self.dist[a][case[a]] += 1

        def remove_completed_cases(date):
            '''
            Function to remove cases that have been completed till a date
            '''
            remove_idx = []
            for idx, case in enumerate(self.cases):
                if date > case["DISPDATE"]:
                    remove_idx.append(idx)
            self.cases = [case[i] for i in range(len(self.cases)) if i not in remove_idx]

        def remove_last_case():
            """
            removes the final case from self.cases and updates the local
            distribution accordingly
            """
            case = self.cases.pop()
            for a in self.dist:
                self.dist[a][case[a]] -= 1

        def update_counts(case):
            # # TODO:
            """
            Updates the global distribution with the cases from "year" using dropout
            """
            self.year_dists[year] = year_dist(year)
            # attr = ["sex", "race", "age", "is_citizen", "educ", "crime", "crim_hist", "counsel"]
            for a in self.global:
                for key in self.global[a]:
                    self.global[a][key] = self.year_dists[year][a][key] + self.weight*self.global[a][key]

class Case:
    def __init__(self, sex, race, age, is_citizen, educ, crime, crim_hist, counsel):
        self.file_date = file_date # FILEDATE
        # ["MONSEX", "NEWRACE", "AGE", "CITIZEN", "NEWEDUC", "XFOLSOR", "CRIMPTS", "FCOUNSEL"]
        self.attr = {"sex": sex, "race": race, "age": age, "is_citizen": is_citizen, "educ": educ,
                     "crime": crime, "crim_hist": crim_hist, "counsel": counsel}


class District:
    def __init__(self, timeframe, weight=0.9): # path expected to be "justfair_dataset.csv"
        self.timeframe = timeframe # time stops after which we update distributions
        self.weight = weight

        self.global = {"sex": defaultdict(int), "race": defaultdict(int), "age": defaultdict(int),
                     "is_citizen": defaultdict(int), "educ": defaultdict(int),
                     "crime": defaultdict(int), "crim_hist": defaultdict(int), "counsel": defaultdict(int)}
        self.year_dists = defaultdict(int)
        self.global = self.init_global()


    def year_dist(year):
        """
        Computes the marginals for the year
        """
        tmp = df[df["FILEDATE"].year == year.year]
        #tmp.groupby(["col1","col2"]).size()
        # tmp["col"].value_counts()
        dist = {"sex": defaultdict(int), "race": defaultdict(int), "age": defaultdict(int),
                     "is_citizen": defaultdict(int), "educ": defaultdict(int),
                     "crime": defaultdict(int), "crim_hist": defaultdict(int), "counsel": defaultdict(int)}
        # attr = ["sex", "race", "age", "is_citizen", "educ", "crime", "crim_hist", "counsel"]
        for a in self.global:
            dist[a] = tmp.value_counts().to_dict()
        return dist


    def discrete_summed_mean_times(df,groups,time_cols):
        """
        Computes conditional distribution over the groups summing over all of the
        columns in time_cols. both groups and time_cols should be lists.
        Each group in groups should be discrete/categorical
        """
        temp = df.dropna(subset = groups)
        temp['total_time'] = temp[time_cols].sum(axis=1)
        grouped = temp.groupby(groups)
        return grouped['total_time'].mean()


    def init_global():
        """
        Initializes the global distributions using the years ____
        """
        end_year = int(self.timeframe[0].year)
        start_year = 2000
        # self.year_dists[start_year] = year_dist(start_year)
        # self.global = self.year_dists[start_year]
        for year in range(start_year, end_year):
            update_global(year)


    def update_global(year):
        """
        Updates the global distribution with the cases from "year" using dropout
        """
        self.year_dists[year] = year_dist(year)
        # attr = ["sex", "race", "age", "is_citizen", "educ", "crime", "crim_hist", "counsel"]
        for a in self.global:
            for key in self.global[a]:
                self.global[a][key] = self.year_dists[year][a][key] + self.weight*self.global[a][key]


    def process_case(case, judges):
        # send in case
        # each case has a filedate
        # use file_date to clear out judge queues
        # assign case
        # ["MONSEX", "NEWRACE", "AGE", "CITIZEN", "NEWEDUC", "XFOLSOR", "CRIMPTS", "FCOUNSEL"]

        # clear out completed cases
        date = case["FILEDATE"]
        for judge in judges:
            judge.remove_completed_cases(date)

        # compute current metric
        judge_dists = judges.map(lambda j: j.dist)
        evals = metric_eval(judge_dists, self.global)

        #  compute metric after hypothetically adding the case
        for judge in judges:
            judge.add_case(case)
        after_evals = metric_eval(judge_dists, self.global)

        # find the maximum decrease in the metric
        diffs = [curr-after for curr,after in zip(evals, after_evals)]
        assign_idx = index(max(diffs))

        # remove the case from all judges except the one to whom it was assigned
        # (i.e.) the one maximimizing the decrease in the metric
        for j_idx in range(0,len(judges)):
            if j_idx != assign_idx:
                judges[j_idx].remove_last_case()

        # ss.zscore(array) to compute zscore for each element





# df = pd.read_csv("justfair_dataset.csv") # takes forever
# Model(1,df)
# Model(2,df)
# Model(3,df)