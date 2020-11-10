import pandas as pd
import numpy as np

def load_and_process(csv_url):
    df = (
        pd.read_csv(csv_url)
        .rename(columns = {'ver':'version_num','sup_devices.num':'sup_devices_num','ipadSc_urls.num':'screenshot_num','lang.num':'lang_num'})
        .sort_values(by = ['user_rating','user_rating_ver','rating_count_tot','rating_count_ver'], ascending = False)
        .reset_index()
        .loc[:,'id':'lang_num']
        .loc[lambda x: x['rating_count_tot'] > 0]
    )
    
    return df