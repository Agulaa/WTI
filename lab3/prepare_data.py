import pandas as pd
import json
file_name_1 = "../user_ratedmovies.dat"
file_name_2 = "../movie_genres.dat"

def _load_data_from_file(filename, usecols):
    """
    Loading data from file - user_ratedmovies.dat
    :return: DataFrame
    """

    data = pd.read_csv(filename, sep="\t", usecols=usecols)
    return data

def change_rows_to_dic(data, row):
    """
    Changing rows to dic - its important because next
    will be change dic to json
    :param row: row from data frame
    :return: dictionary with data from row
    """
    return data.iloc[row].to_dict()


def join_dataframe():
    """
    Join two data frame and create new data frame
    :return:
    """
    df1 = pd.read_csv(file_name_1, sep="\t", usecols=["userID", "movieID", "rating"], nrows=100)
    df2 = _load_data_from_file(file_name_2, ["movieID", "genre"])

    df2["dummy_column"] = 1
    df_pivoted = df2.pivot_table(index="movieID", columns="genre", values="dummy_column") #The levels in the pivot table will be stored in MultiIndex objects
                                                                                        #  (hierarchical indexes) on the index and columns of the result DataFrame.
    df_pivoted = df_pivoted.fillna(0)


    df = pd.merge(df1, df_pivoted, on=["movieID"])

    df.columns = ["genres_" + name if name not in df.columns[:3] else name for name in df.columns]

    return df

#df = join_dataframe()
#print(df.head())
# df.to_csv("ratings_data")

df = pd.read_csv("ratings_data")
df = df.drop(["Unnamed: 0"], axis=1)



def prepare_all_data_to_send():
    """
    Preparing all data (json documnet) to send.
    :return: json
    """
    DATA = []
    iterrow = df.iterrows()
    for i in iterrow:
        dict_to_send = change_rows_to_dic(df, i[0])
        DATA.append(dict_to_send)

    return json.dumps(DATA)


def prepare_data_to_send(n):
    """
    Preparing n data (n rows) to send
    :param n: number of rows
    :return: json
    """
    DATA = []

    iterrow = df.iterrows()
    for i in iterrow:
        dict_to_send = change_rows_to_dic(df, i[0])
        DATA.append(dict_to_send)
        if i[0] == n:
            break

    return json.dumps(DATA)


def get_mean_of_all_users():
    """
    Get mean of all column (all genres) in dataframe
    :return:
    """

    mean = [df[name].mean() for name in df.columns.values[3:]]
    data = [{name:m} for name, m in zip(df.columns.values[3:], mean)]
    return json.dumps(data)


def get_mean_of_one_user(user_id):
    """
    Get mean of all columns (all genres) for current user_id
    :param user_id: user id
    :return:
    """
    df_groupe = df.groupby("userID").mean()
    data = df_groupe.iloc[user_id][3:].to_dict()
    return json.dumps(data)


print(df.head())

#get_mean_of_one_user(75)