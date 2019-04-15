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
    df1 = pd.read_csv(file_name_1, sep="\t", usecols=["userID", "movieID", "rating"], nrows=1000)
    df2 = pd.read_csv(file_name_2, sep="\t", usecols=["movieID", "genre"])
    merged = df1.merge(df2, on='movieID')
    # #merged.to_csv("merged.csv", sep='\t')
    df2["dummy_column"] = 1
    df_pivoted = df2.pivot_table(index="movieID", columns="genre", values="dummy_column") #The levels in the pivot table will be stored in MultiIndex objects
                                                                                            #  (hierarchical indexes) on the index and columns of the result DataFrame.
    df_pivoted = df_pivoted.fillna(0) # change Nan to 0


    df = pd.merge(df1, df_pivoted, on=["movieID"])
    genres = df.columns[3:-1].values

    #df.columns = ["genres_" + name if name not in df.columns[:3] else name for name in df.columns]
    #Genres_with = df.columns[3:-1].values
    users_id = df['userID'].unique()

    return df,merged, genres, users_id


#ZADANIE 2
def DataFrame_to_dict(df):
    """
    Change row dataframe to dict
    :param df: dataframe
    :return: dicts with records
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

#additional function
def change_nan(dict):
    """
    Change value in dict -> Nan to 0.0
    :param dict: dict with nan values
    """

    for k,v in dict.items():
        if np.isnan(v):
            dict[k] = 0.0
        else:
            dict[k] = v

def get_all_genres_from_df(df):
    return  df.columns[3:-1].values


#ZADANIE 5
def get_mean_of_all_genres(df, merged):
    """
    Calculate mean for all genres.
    :param df: data frame with rating
    :param all_genres: only genres
    :return: dict with mean for all genres, data frame with update rating
    """
    all_genres = get_all_genres_from_df(df)
    mean_genres = {}
    for genres in all_genres:
        mean_genres[genres] = df['rating'][df[genres] == 1].mean()


    change_nan(mean_genres) # change Nan value


    for genres in all_genres:
        merged.loc[merged.genre == genres, 'rating'] = merged.loc[merged.genre == genres, 'rating'].map(lambda x : x - mean_genres[genres])

    return mean_genres 


#ZADANIE 6
def get_mean_for_user(df,genres, userID):
    #PROFIL UŻYTWKONIKA# 
    """
    Calculate mean for given userID
    :param genres: only name genres
    :param merged_df: updated dataframe
    :param userID: id
    :return: dict with mean for all genres
    """


    mean_for_user = {}
    for genre in genres:
        mean_for_user[genre] = df[(df['userID'] == userID ) & (df['genre'] == genre)]['rating'].mean()
    change_nan(mean_for_user)
    return mean_for_user

#ZADANIE 7
def get_vector_for_ueser(df, genres, userID, mean_genres):
    """
    Update vector for user
    :param mean_for_user: dict with mean for user
    :param mean_genres: mean genres
    :return: new mean for user and vector with only mean
    """
    mean_for_user = get_mean_for_user(df, genres, userID)

    dict_mean_for_user = {}
    for genres, mean in mean_for_user.items():
        if mean > 0.0:
            dict_mean_for_user[genres] = mean_genres[genres] - mean
        else:
            dict_mean_for_user[genres] = mean


    mean_array = [v for v in dict_mean_for_user.values()]
    mean_array = np.array(mean_array)

    return dict_mean_for_user, mean_array

def create_matrix_all_user(users_id,genres,df, mean_genres):
    data_dic_with_mean = []
  
    for id in users_id:
        mean_for_user = get_mean_for_user(df,genres, id)

        dict_mean_for_user, mean_array = get_vector_for_ueser(df, genres, id, mean_genres)
        data_dic_with_mean.append(dict_mean_for_user)
       

    dataframe_with_mean = dict_to_DataFrame(data_dic_with_mean)
    dataframe_with_mean['userID'] = users_id
    return dataframe_with_mean


if __name__ == '__main__':
    file_name_1 = "../user_ratedmovies.dat"
    file_name_2 = "../movie_genres.dat"
    df, merged, genres, users_id = join_dataframe(file_name_1, file_name_2)

    mean_genres = get_mean_of_all_genres(df, merged) #update merged dataframe 
    print(merged.head())
  
    data_dic_with_mean, data_array_mean = create_matrix_all_user(users_id, genres,merged)
    print(data_dic_with_mean.head())
   
