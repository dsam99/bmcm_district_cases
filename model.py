import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.stats as ss

class Judge:
    def __init__(self, name):
        self.name = name
        self.dist = {"sex": [], "race": [], "age": [], "is_citizen": [], "educ": [],
                            "crime": [], "crim_hist": [], "counsel": []}


class Case:
    def __init__(self, sex, race, age, is_citizen, educ, crime, crim_hist, counsel):
        self.file_date = file_date # FILEDATE
        # [MONSEX, NEWRACE, AGE, CITIZEN, NEWEDUC, XFOLSOR, CRIMPTS, FCOUNSEL]
        self.attr = {"sex": sex, "race": race, "age": age, "is_citizen": is_citizen, "educ": educ,
                     "crime": crime, "crim_hist": crim_hist, "counsel": counsel}


class District:
    def __init__(self, name, df, timeframe,
                ageframe=[15,30,50,65,80,150],
                crimframe=[-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,25,1000]): # path expected to be "justfair_dataset.csv"
        self.name = name
        self.df = df[df["CIRCDIST"] == self.name]
        self.df = self.df[["FILEDATE","MONSEX", "NEWRACE", "AGE", "CITIZEN", "NEWEDUC","XFOLSOR", "CRIMPTS", "FCOUNSEL"]]
        self.df["FILEDATE"] = pd.to_datetime(df["FILEDATE"], format='%m/%d/%Y')
        self.df.sort_values("FILEDATE",inplace=true)
        self.df["AGE"] = pd.cut(df["AGE"], ageframe)
        self.df["CRIMPTS"] = pd.cut(df["CRIMPTS"],crimframe)
        self.timeframe = timeframe # time stops after which we update distributions
        self.dist = {"sex": [], "race": [], "age": [], "is_citizen": [], "educ": [],
                            "crime": [], "crim_hist": [], "counsel": []}

        # df["APPDATE"] = pd.to_datetime(df["APPDATE"], format='%m/%d/%Y') (use to convert column to datetimes)

    def init_global():
        start_time = timeframe[0]
        # [MONSEX, NEWRACE, AGE, CITIZEN, NEWEDUC, XFOLSOR, CRIMPTS, FCOUNSEL]
        for idx, row in self.df.iterrows():
            if row["FILEDATE"] < start_time:
                self.dist["sex"][row["MONSEX"]] += 1
                self.dist["sex"][row["MONSEX"]] += 1
                self.dist["sex"][row["MONSEX"]] += 1
            else:
                print()

    def update_distribution():
        # # TODO:




















# df = pd.read_csv("justfair_dataset.csv") # takes forever
# Model(1,df)
# Model(2,df)
# Model(3,df)