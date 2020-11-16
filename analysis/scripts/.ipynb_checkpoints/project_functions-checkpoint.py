import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_process(csv_url):
    df = (
        pd.read_csv(csv_url)
        .rename(columns = {'ver':'version_num','sup_devices.num':'sup_devices_num','ipadSc_urls.num':'screenshot_num','lang.num':'lang_num'})
        .sort_values(by = ['user_rating','user_rating_ver','rating_count_tot','rating_count_ver'], ascending = False)
        .drop(columns = ['rating_count_ver','user_rating_ver'],axis = 1)
        .reset_index()
        .loc[:,'id':'lang_num']
        .loc[lambda x: x['rating_count_tot'] > 0]
    )
    
    return df

def describe(df):
    df = (
     df.assign(size_Megabytes = lambda x: round(x['size_bytes']/1024/1024,2))
     .describe()
     .drop(columns = ['id','size_bytes'],axis = 1)
     )
    return df

def count_per_genre_plot(df):

    sns.set_theme(font_scale = 1.2, style = 'darkgrid')
    plt.figure(figsize = (12,6))
    plot = (sns.countplot(data = df, y = 'prime_genre')
    .set(ylabel = 'prime genre')
    )
    
    return plot