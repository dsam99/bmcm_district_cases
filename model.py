import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.stats as ss
from collections import defaultdict
import random

import metric

# mean judge assumption

class Judge:
    def __init__(self, name, keys, feats):
        self.name = name
        self.dist = {k: 0 for k in keys}
        self.features = feats
        self.case_count = 0

    def add_case(self, case):
        '''
        Function to add a case to the queue and update distribution
        '''
        self.case_count += 1
        for f in self.features:
            self.dist[case[f]] += 1

    def remove_case(self, case):
        """
        removes the final case from self.cases and updates the local
        distribution accordingly
        """
        self.case_count -= 1
        for f in self.features:
            self.dist[case[f]] -= 1

class Case:
    def __init__(self, sex, race, age, is_citizen, educ, crime, crim_hist, counsel):
        self.file_date = file_date # FILEDATE
        # ["MONSEX", "NEWRACE", "AGE", "CITIZEN", "NEWEDUC", "XFOLSOR", "CRIMPTS", "FCOUNSEL"]
        self.attr = {"sex": sex, "race": race, "age": age, "is_citizen": is_citizen, "educ": educ,
                     "crime": crime, "crim_hist": crim_hist, "counsel": counsel}


def process_case(subattributes, case, judges):
    # send in case
    # each case has a filedate
    # use file_date to clear out judge queues
    # assign case
    # ["MONSEX", "NEWRACE", "AGE", "CITIZEN", "NEWEDUC", "XFOLSOR", "CRIMPTS", "FCOUNSEL"]

    # compute current metric
    judge_dists = {j.name: j.dist for j in judges}
    # evals, _ = metric.eval_metric(subattributes, judge_dists, kl=False)

    #  compute metric after hypothetically adding the case
    after_evals = []
    for judge in judges:
        judge.add_case(case)
        after_evals.append(metric.tv_metric(subattributes, judge_dists)[0])
        judge.remove_case(case)

    # find the maximum decrease in the metric
    assign_idx = np.argmin(after_evals)
    judges[assign_idx].add_case(case)


def assign_uniformly(case,judges):
    random.choice(judges).add_case(case)


def assign_by_name(case,judges):
    for judge in judges:
        if judge.name == case["judge"]:
            judge.add_case(case)
            break
