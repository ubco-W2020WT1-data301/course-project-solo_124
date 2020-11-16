import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas_profiling

def load_and_process(csv_url):
    df = (
        pd.read_csv(csv_url)
        .rename(columns = {'ver':'version_num','sup_devices.num':'sup_devices_num','ipadSc_urls.num':'screenshot_num','lang.num':'lang_num'})
        .sort_values(by = ['user_rating','user_rating_ver','rating_count_tot','rating_count_ver'], ascending = False)
        .drop(columns = ['rating_count_ver','user_rating_ver'],axis = 1)
        .reset_index()
        .loc[:,'id':'lang_num']
        .loc[lambda x: x['rating_count_tot'] > 0]
        .assign(size_Megabytes = lambda x: round(x['size_bytes']/1024/1024,2))
    )
    
    return df

def describe(df):
    df = (
     df.describe()
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

def correlation_user_rating(df):
    sns.set_theme(font_scale = 1.2, style = 'darkgrid')
    plot = sns.pairplot(
    df,
    y_vars=['user_rating'],
    x_vars=['user_rating','size_Megabytes','price','sup_devices_num','screenshot_num','lang_num'],
    )
    return plot

def q1_genre_rating(df):
    genres_ratings = {}
    user_rating = [0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
    genres = df['prime_genre'].unique()
    for genre in genres:
        ratings= []
        for rate in user_rating:
            dataframe = df.loc[(df['prime_genre'] == genre)&(df['user_rating'] == rate)]
            ds = dataframe.shape
            ratings.append(ds[0])
        genres_ratings[genre] = ratings
    dataframe = pd.DataFrame(genres_ratings)
    dataframe = (dataframe.transpose()
                .rename(columns = {0:0.0,1:0.5,2:1.0,3:1.5,4:2.0,5:2.5,6:3.0,7:3.5,8:4.0,9:4.5,10:5.0})
                .assign(total = lambda x: x[0.0]+x[0.5]+x[1.0]+x[1.5]+x[2.0]+x[2.5]+x[3.0]+x[3.5]+x[4.0]+x[4.5]+x[5.0])
                )
    return dataframe

def q1_enre_rating_boxplot(df):
    plt.figure(figsize = (12,8))
    plot = sns.boxplot(data = df, x = 'user_rating', y = 'prime_genre', width = 0.8)
    return plot

def q1_answer(df):
    df = (df.drop(columns=[0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5], axis = 1)
            .transpose()
            .drop(columns = ['Shopping',
                      'Finance',
                      'Education',
                      'Business',
                      'Utilities',
                      'Reference',
                      'Lifestyle',
                      'Catalogs',
                      'News',
                      'Entertainment',
                      'Sports',
                      'Weather',
                      'Medical',
                      'Travel',
                      'Book',
                      'Social Networking',
                      'Navigation',
                      'Food & Drink'],axis = 1)
            .transpose()
         )

    return df
        
def q1_answer_plot(df):
    genres = ['Games','Photo & Video','Health & Fitness','Productivity','Music']

    for genre in genres:
        sns.set_theme(font_scale = 1, style = 'darkgrid')
        plt.figure(figsize = (12,0.6))
        plt.yticks(rotation=90)
        dataframe = df.loc[df['prime_genre'] == genre]
        sns.countplot(y='prime_genre',data = dataframe).set(ylabel = '',xlabel = '')
        dataframe = dataframe.loc[df['user_rating'] == 5.0]
        sns.countplot(y='prime_genre',data = dataframe).set(ylabel = '',xlabel = '')
    

def wrangling_data(df):
    df = df.drop(columns = ['id','track_name','sup_devices_num','cont_rating','version_num','screenshot_num'],axis = 1)
    return df

def q2_joint_plot(df):
    plot = sns.jointplot(data = df, x = 'user_rating', y = 'size_Megabytes')
    return plot

def q2_count_plot(df):
    plot = sns.countplot(x='user_rating',data =df)
    return plot

def q2_size_mean_table(df):
    ratings = []
    means = []
    user_ratings = df['user_rating'].unique()
    for user_rating in user_ratings:
        dataframe = df.loc[df['user_rating'] == user_rating]
        means.append(dataframe['size_Megabytes'].mean())
        ratings.append(user_rating)
    
    rating_size = {'user_rating':ratings,'size means':means}   
    dataframe = pd.DataFrame(rating_size)
    return dataframe

def q3_joint_plot(df):
    plot = sns.jointplot(data = df, x = 'user_rating', y = 'price')
    return plot

def q3_price_mean_table(df):
    ratings = []
    means = []
    user_ratings = df['user_rating'].unique()
    for user_rating in user_ratings:
        dataframe = df.loc[df['user_rating'] == user_rating]
        means.append(dataframe['price'].mean())
        ratings.append(user_rating)
    
    rating_size = {'user_rating':ratings,'price means':means}   
    dataframe = pd.DataFrame(rating_size)
    return dataframe

def q4_joint_plot(df):
    plot = sns.jointplot(data = df, x = 'user_rating', y = 'lang_num')
    return plot

def q4_lang_mean_table(df):
    ratings = []
    means = []
    user_ratings = df['user_rating'].unique()
    for user_rating in user_ratings:
        dataframe = df.loc[df['user_rating'] == user_rating]
        means.append(dataframe['lang_num'].mean())
        ratings.append(user_rating)
    
    rating_size = {'user_rating':ratings,'language supported means':means}   
    dataframe = pd.DataFrame(rating_size)
    return dataframe

def lm_plot(df,y_value):
    plot = sns.lmplot(x='user_rating', y=y_value, data=df)
    return plot

def profiling(df):
    prof = pandas_profiling.ProfileReport(df)
    prof.to_file(output_file='../../data/processed/output.html')