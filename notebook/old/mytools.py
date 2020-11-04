import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib as pl
from collections import defaultdict

def get_stats(dsi):
    i, dsi = dsi
    stats = defaultdict(lambda: defaultdict(lambda: None))
    for df in dsi:
        iw, costw, an, mean, meann, meanm, median, mediann, medianm = df.mean()
        stats[costw][iw] = {'initial-w':iw, 'k':i, 'costw':costw,'none-anonymity': an,'mean-min': meann,'max-mean': meanm,'median-mean': mediann,'max-median': medianm}
    return stats
    
    
def scater(dfs):
    for i, df in dfs.items():
        df.plot.scatter(x='initial-w',y='max-mean', title=f'In weight {i}')
	
def get_data_frames(stats, max_range=3):
    columns = stats[1][135].keys()
    data = {}
    for cw in range(1,4+1):
        dat = defaultdict(lambda: [])
        for s in stats[cw].values():
            for c in columns:
                dat[c].append(s[c])
        data[cw] = dat
    dfs = {}

    for cw in range(1, max_range+1):
        dfs[cw] = pd.DataFrame(data=data[cw])
    return dfs
    
def show(stats, max_range=3):
    scater(get_data_frames(stats, max_range))
