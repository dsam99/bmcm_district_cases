import pandas as pd

df = pd.read_csv("justfair_dataset.csv")

def judge_mean_times(df,judge_col,time_col):
    """
    Calculates the mean case time for each judge (as identified by judge_col)
    using time_col
    """
    temp = df.dropna(subset = [judge_col])
    group = temp.groupby(judge_col)
    return group[time_col].mean()

means = judge_mean_times(df,"judge","INT2") # we should decide on which columns specifically we want to use
print(means)
# means.to_csv("judge_means.csv") # don't want to lose the histogram by overwriting the file
