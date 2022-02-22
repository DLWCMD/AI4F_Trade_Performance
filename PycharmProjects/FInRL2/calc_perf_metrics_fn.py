import pandas as pd
import numpy as np
from pathlib import Path
'''
Data columns:
#_trades', '#_wins', '#_losses', 'wins_total_value', 'wins_avg_value',
       'losses_total_value', 'losses_avg_value'],
'''
''' metrics:
% wins, % losses, r_#wins/#losses
wins_totval, losses_totval, r_wins_totval/losses_totval
r_wins_avgval/losses_avg_val

'''
metric_names = ['pct_wins','pct_losses','r_wl_cnt','r_wl_totval','r_wl_avgval']

def calc_metric_pct_wins(data,
                         tpm_hist=None):
    #metric = 'pct_wins'
    m = sum(data['#_wins']) / sum(data['#_trades'])
    return m

def calc_metric_pct_losses(data,
                           tpm_hist=None):
    #metric = 'pct_losses'
    m = sum(data['#_losses']) / sum(data['#_trades'])
    return m

def calc_metric_r_wl_cnt(data,
                         tpm_hist):
    # metric = r_wl_cnt
    tpm_mult = 1
    # account for no losses
    n_losses = sum(data['#_losses'])
    # avoid division by zero
    r_no_losses = 25
    if n_losses == 0:
        try:
            return max(tpm_hist.values()) * tpm_mult
        except ValueError:
            return r_no_losses
    m = sum(data['#_wins']) / n_losses
    return m

def calc_metric_r_wl_totval(data,
                 tpm_hist):
    # metric == 'r_wl_totval':
    tpm_mult = 1
    totval_no_losses = 25
    n_losses = sum(data['#_losses'])
    if n_losses == 0:
        try:
            return max(tpm_hist.values()) * tpm_mult
        except ValueError:
            return totval_no_losses
    m = sum(data['wins_total_value']) / sum(data['losses_total_value'])
    m = abs(m)
    return m

def calc_metric_r_wl_avgval(data,tpm_hist):
    # metric = 'r_wl_avgval'
    tpm_mult = 1
    avgwl_no_losses = 25
    n_losses = sum(data['#_losses'])
    if n_losses == 0:
        try:
            return max(tpm_hist.values()) * tpm_mult
        except ValueError:
            return avgwl_no_losses
    avg_w = sum(data['wins_total_value']) / sum(data['#_wins'])
    avg_l = sum(data['losses_total_value']) / n_losses
    m = abs(avg_w / avg_l)
    return m

md = {metric_names[0]:calc_metric_pct_wins,
      metric_names[1]:calc_metric_pct_losses,
      metric_names[2]:calc_metric_r_wl_cnt,
      metric_names[3]:calc_metric_r_wl_totval,
      metric_names[4]:calc_metric_r_wl_avgval}

data_fn = 'perf_results.csv'
data_dir = 'resources'
data_fp=Path(data_dir) / data_fn


def tst_code():
    # For testing: in actual use, data is passed from objective function
    print(data_fp)
    perf_data_df = pd.read_csv(data_fp, index_col=0)
    print(perf_data_df.shape)
    # placeholder for tp history attribute
    tpm_hist = pd.Series(np.random.randint(25, 75, size=10))

    for m_name, m_func in md.items():
        print(f'Calculating metric {m_name}')
        m = m_func(perf_data_df,
                   tpm_hist)
        print(m)

if __name__ == '__main__':
    tst_code()
