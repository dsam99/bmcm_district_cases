import pandas as pd
import matplotlib as plt

# PRISTOT
# DEFCONSL
# FCOUNSEL

def discrete_mean_times(df,group,time_col):
    """
    Computes conditional distribution over the group
    """
    temp = df.dropna(subset = [group])
    grouped = temp.groupby(group)
    return grouped[time_col].mean()


def discrete_summed_mean_times(df,group,time_cols):
    """
    Calculates the mean case time for each judge (as identified by judge_col)
    using sum of time_cols (time_cols is a list of column names)
    """
    temp = df.dropna(subset = [group])
    temp['total_time'] = temp[time_cols].sum(axis=1)
    grouped = temp.groupby(group)
    return grouped['total_time'].mean()


def judge_summed_mean_times(df,judge_col,time_cols):
    """
    Calculates the mean case time for each judge (as identified by judge_col)
    using sum of time_cols (time_cols is a list of column names)
    """
    temp = df.dropna(subset = [judge_col])
    temp['total_time'] = temp[time_cols].sum(axis=1)
    grouped = temp.groupby(judge_col)
    return grouped['total_time'].mean()


def judge_mean_times(df,judge_col,time_col):
    """
    Calculates the mean case time for each judge (as identified by judge_col)
    using just time_col
    """
    temp = df.dropna(subset = [judge_col])
    grouped = temp.groupby(judge_col)
    return grouped[time_col].mean()


if __name__ == "__main__":
    df = pd.read_csv("justfair_dataset.csv")
    summed_means = judge_summed_mean_times(df,"judge",['INT1','INT2','INT3'])
    summed_means.plot.hist()
    means = judge_mean_times(df,"judge","INT2") # we should decide on which columns specifically we want to use
    means.plot.hist()

    plt.pyplot.show()
    #summed_means.to_csv("judge_means.csv") # don't want to lose the histogram by overwriting the file
    # df = df[df['judge'] == 'Wilma A. Lewis']
