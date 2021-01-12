import pandas as pd
import matplotlib as plt

# PRISTOT
# DEFCONSL
# FCOUNSEL

# def discrete_mean_times(df,group,time_col):
#     """
#     Computes conditional distribution over the group using one time column
#     """
#     temp = df.dropna(subset = [group])
#     grouped = temp.groupby(group)
#     return grouped[time_col].mean()


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


if __name__ == "__main__":
    # for example ....
    df = pd.read_csv("justfair_dataset.csv")
    summed_means = discrete_summed_mean_times(df,["judge","CRIMHIST"],['INT1','INT2','INT3'])
    summed_means.plot.hist(bins=20)
    means = discrete_summed_mean_times(df,["judge","CRIMHIST"],["INT2"]) # we should decide on which columns specifically we want to use
    means.plot.hist()
    plt.pyplot.show()
    #summed_means.to_csv("judge_means.csv") # don't want to lose the histogram by overwriting the file
    # df = df[df['judge'] == 'Wilma A. Lewis']
