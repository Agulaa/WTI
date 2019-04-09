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
    # merged = df1.merge(df2, on='movieID')
    # #merged.to_csv("merged.csv", sep='\t')
    df2["dummy_column"] = 1
    df_pivoted = df2.pivot_table(index="movieID", columns="genre", values="dummy_column") #The levels in the pivot table will be stored in MultiIndex objects
                                                                                            #  (hierarchical indexes) on the index and columns of the result DataFrame.
    df_pivoted = df_pivoted.fillna(0) # change Nan to 0


    df = pd.merge(df1, df_pivoted, on=["movieID"])
    Genres = df.columns[3:-1].values

    df.columns = ["genres_" + name if name not in df.columns[:3] else name for name in df.columns]
    Genres_with = df.columns[3:-1].values
    users_id = df['userID'].unique()

    return df,  Genres, Genres_with, users_id


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


#ZADANIE 5
def get_mean_of_all_genres(df, all_genres, all_genres_with):
    """
    Calculate mean for all genres.
    :param df: data frame with rating
    :param all_genres: only genres
    :param all_genres_with: genres with word genres_...
    :return: dict with mean for all genres, data frame with update rating
    """
    mean_genres = {}
    for genres, g_with in zip(all_genres,all_genres_with):
        mean_genres[genres] = df['rating'][df[g_with] == 1].mean()


    change_nan(mean_genres) # change Nan value

    df1 = pd.read_csv("../user_ratedmovies.dat", sep="\t", usecols=["userID", "movieID", "rating"], nrows=1000)
    df2 = pd.read_csv(file_name_2, sep="\t", usecols=["movieID", "genre"])
    merged = df1.merge(df2, on='movieID')
    merged = merged.fillna(0)

    for genres in all_genres:
        merged.loc[merged.genre == genres, 'rating'] = merged.loc[merged.genre == genres, 'rating'].map(lambda x : x - mean_genres[genres])

    return mean_genres, merged


#ZADANIE 6
def get_mean_for_user(genres, merged_df, userID):
    """
    Calculate mean for given userID
    :param genres: only name genres
    :param merged_df: updated dataframe
    :param userID: id
    :return: dict with mean for all genres
    """
    mean_for_user = {}
    for genre in genres:
        mean_for_user[genre] = merged_df[(merged_df['userID'] == userID ) & (merged_df['genre'] == genre)]['rating'].mean()
    change_nan(mean_for_user)
    return mean_for_user

#ZADANIE 7
def get_vector_for_ueser(mean_for_user, mean_genres):
    """
    Update vector for user
    :param mean_for_user: dict with mean for user
    :param mean_genres: mean genres
    :return: new mean for user and vector with only mean
    """
    #print(mean_genres)
    new_mean_for_user = {}
    for genres, mean in mean_for_user.items():
        if mean > 0.0:
            new_mean_for_user[genres] = mean_genres[genres] - mean
        else:
            new_mean_for_user[genres] = mean


    ar = [v for v in new_mean_for_user.values()]
    ar = np.array(ar)

    return new_mean_for_user, ar

def create_matrix_all_user(users_id, Genres, merged):
    data = []
    data_ar = []
    for id in users_id:
        mean_for_user = get_mean_for_user(Genres, merged, id)

        new_mean_for_user, ar = get_vector_for_ueser(mean_for_user, mean_genres)
        data.append(new_mean_for_user)
        data_ar.append(ar)

    return data, data_ar


if __name__ == '__main__':
    file_name_1 = "../user_ratedmovies.dat"
    file_name_2 = "../movie_genres.dat"
    df, Genres, Genres_with, users_id = join_dataframe(file_name_1, file_name_2)
    mean_genres, merged = get_mean_of_all_genres(df,Genres ,Genres_with)

   # data = DataFrame_to_dict(df)

    data, data_ar = create_matrix_all_user(users_id, Genres, merged)
    data_user = dict_to_DataFrame(data)
    data_user['userID'] = users_id
    data_user.set_index("userID", inplace=True, drop=True)
    print(data_user)
