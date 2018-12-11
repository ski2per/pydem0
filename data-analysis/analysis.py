import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import re
import os.path
import pandas as pd

# SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample")
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "raw2")

font = fm.FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")


def get_sample_list():
    return os.listdir(SAMPLE_DIR)


def get_delay(sample):
    # mat = re.search("[0-9]+ms", sample)
    mat = re.search("[0-9]+", sample)
    if mat:
        delay = mat.group(0)
    else:
        delay = ""

    return delay


def plot_all_sample():
    all_sample = pd.DataFrame()
    samples = get_sample_list()

    for sample in samples:
        delay = get_delay(sample)
        if not delay:
            continue

        df = pd.read_json(os.path.join(SAMPLE_DIR, sample), lines=True)
        df["elapse"] = df["endTime"] - df["startTime"]
        # df.drop(["endTime", "startTime", "invokeStatus", "valueAfter", "valueBefore"],axis=1)
        all_sample = pd.concat([all_sample, df["elapse"]], axis=1)
        all_sample = all_sample.rename(columns={"elapse": delay})


    all_sample.columns = all_sample.columns.astype('int64')
    # all_sample[:5].plot(sort_columns=True)
    # all_sample = all_sample.reindex_axis(sorted(all_sample.columns), axis=1)

    all_sample = all_sample.reindex(sorted(all_sample.columns), axis=1)

    all_sample[:200].plot(subplots=True, layout=(10,2), figsize=(10,8), sharex=True, ylim=(0, 15))
    # ax = all_sample[:200].plot()
    # ax.set_xlabel("test")

    # print(ax)


    plt.show()


def plot_all_mean():
    sample_mean = {}

    samples = get_sample_list()

    for sample in samples:
        delay = get_delay(sample)
        if not delay:
            continue

        df = pd.read_json(os.path.join(SAMPLE_DIR, sample), lines=True)
        df["elapse"] = df["endTime"] - df["startTime"]
        # sample_mean[int(delay)] = df["elapse"].mean()
        sample_mean[delay] = df["elapse"].mean()

    s = pd.Series(sample_mean)

    # print(s.index)
    s.index = s.index.astype("int64")
    # s.sort_index().plot.bar()
    ax = s.sort_index().plot()
    ax.set_xlabel("网络延时(毫秒)", fontproperties=font)
    ax.set_ylabel("成功交易平均耗时(秒)", fontproperties=font)

    print(s.sort_index())
    plt.show()





if __name__ == "__main__":
    plot_all_sample()
    # plot_all_mean()
