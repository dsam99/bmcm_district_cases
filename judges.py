import pandas as pd

def judge_summed_mean_times(df,judge_col,time_cols):
    """
    Calculates the mean case time for each judge (as identified by judge_col)
    using sum of time_cols
    """
    temp = df.dropna(subset = [judge_col])
    temp['total_time'] = temp[time_cols].sum(axis=1)
    group = temp.groupby(judge_col)
    return group['total_time'].mean()


def judge_mean_times(df,judge_col,time_col):
    """
    Calculates the mean case time for each judge (as identified by judge_col)
    using just time_col
    """
    temp = df.dropna(subset = [judge_col])
    group = temp.groupby(judge_col)
    return group[time_col].mean()


if __name__ == "__main__":
    df = pd.read_csv("justfair_dataset.csv")
    summed_means = judge_summed_mean_times(df,"judge",['INT1','INT2','INT3'])
    print(summed_means)
    means = judge_mean_times(df,"judge","INT2") # we should decide on which columns specifically we want to use
    #print(means)

    # means.to_csv("judge_means.csv") # don't want to lose the histogram by overwriting the file
    # df = df[df['judge'] == 'Wilma A. Lewis']