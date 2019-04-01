import pandas as pd
import numpy as np
import json

#ZADANIE 1

def join_dataframe(file_name_1, file_name_2):
    """
    Join two data frame to one and return array with genres names.
    :param file_name_1: txt file
    :param file_name_2: txt file
    :return: joined dataframe and array genres
    """
    df1 = pd.read_csv(file_name_1, sep="\t", usecols=["userID", "movieID", "rating"], nrows=100)
    df2 = pd.read_csv(file_name_2, sep="\t", usecols=["movieID", "genre"])
    merged = df1.merge(df2, on='movieID')
    merged.to_csv("merged.csv", sep='\t')
    df2["dummy_column"] = 1
    df_pivoted = df2.pivot_table(index="movieID", columns="genre", values="dummy_column") #The levels in the pivot table will be stored in MultiIndex objects
                                                                                        #  (hierarchical indexes) on the index and columns of the result DataFrame.
    df_pivoted = df_pivoted.fillna(0)


    df = pd.merge(df1, df_pivoted, on=["movieID"])
    Geners1 = df.columns[3:-1].values

    df.columns = ["genres_" + name if name not in df.columns[:3] else name for name in df.columns]
    Geners2 = df.columns[3:-1].values


    return df,  Geners1, Geners2


#ZADANIE 2
def DataFrame_to_dict(df):
    """
    Change row dataframe to dict
    :param df: dataframe
    :return: dicts
    """
    return df.to_dict(orient='records')


#ZADANIE 3
def dict_to_DataFrame(data):
    """
    Change dict to dataframe
    :param data: dict
    :return: dataframe
    """
    return pd.DataFrame.from_dict(data)

def change_nan(dict):

    for k,v in dict.items():
        if np.isnan(v):
            dict[k] = 0.0
        else:
            dict[k] = v


#ZADANIE 5
def get_mean_of_all_genres(df, all_genres1, all_genres2):
    """
    Get mean of all column (all genres) in dataframe
    :return:
    """
    mean_genres = {}
    for genres1, genres2 in zip(all_genres1,all_genres2):
        mean_genres[genres1] = df['rating'][df[genres2] == 1].mean()


    change_nan(mean_genres)

    df1 = pd.read_csv("../user_ratedmovies.dat", sep="\t", usecols=["userID", "movieID", "rating"], nrows=100)
    df2 = pd.read_csv(file_name_2, sep="\t", usecols=["movieID", "genre"])
    merged = df1.merge(df2, on='movieID')
    merged = merged.fillna(0)

    for genres in all_genres1:
        merged.loc[merged.genre == genres, 'rating'] = merged.loc[merged.genre == genres, 'rating'].map(lambda x : x - mean_genres[genres])

    return mean_genres, merged


#ZADANIE 6
def get_mean_for_user(genres, merged_df, userID):
    mean_for_user = {}
    for genre in genres:

        mean_for_user[genre] = merged_df[(merged_df['userID'] == userID ) & (merged_df['genre'] == genre)]['rating'].mean()
    change_nan(mean_for_user)
    return mean_for_user

#ZADANIE 7
def get_vector_for_ueser(mean_for_user, mean_genres):
    print(mean_genres)
    new_mean_for_user = {}
    for genres, mean in mean_for_user.items():
        if mean > 0.0:
            new_mean_for_user[genres] = mean_genres[genres] - mean
        else:
            new_mean_for_user[genres] = mean

    return new_mean_for_user


if __name__ == '__main__':
    file_name_1 = "../user_ratedmovies.dat"
    file_name_2 = "../movie_genres.dat"
    df, Genres1, Genres2 = join_dataframe(file_name_1, file_name_2)
    mean_genres, merged = get_mean_of_all_genres(df,Genres1 ,Genres2)

    data = DataFrame_to_dict(df)

    mean_for_user = get_mean_for_user(Genres1, merged, 75)

    get_vector_for_ueser(mean_for_user,mean_genres )