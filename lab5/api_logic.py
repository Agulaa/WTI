import pandas as pd
from movies import DataFrame_to_dict, join_dataframe, get_mean_of_all_genres, create_matrix_all_user

#powinien umożliwiać ZAPIS kolejnych wierszy tabeli -> POST -> /rating
#powinien umożliwiać ODCZYT  -> GET ->/ratings
#powinien umożliwiać KASOWANIE  -> DELETE ->/ratings
#powinien umożliwiać ODCZYT słownika zawierającego średnie oceny udzielone filmom poszczególnych gatunków -> GET -> /avg-genre-ratings/all-users
#powinien umożliwiać ODCZYT aktualnego profilu użytkownika -> GET ->  /avg-genre-ratings/user<userID>

#DataFrame_to_dict(df): -> zamienia datarfame na listę słowników 
    #return lista słowników
#join_dataframe(file_name_1, file_name_2):  -> tworzy dataframe z userID, movieID, rating, and all genres 
    #return df,merged, genres, users_id
#create_matrix_all_user(users_id,genres,df, mean_genres): -> zwraca macierz z userID, oraz ocenami dla wszytskich gatunków ocenionionych przez usera
    #return dataframe_dic_with_mean, data_array_mean



#PROFIL USERA => powinny być średnie oceny udzielone przez tego użytkownika filmom poszczególnych gatunków
class ApiLogic:

    def __init__(self):
        """
        self.df - dataframe with userID, movieID, rating, allGenres(0 or 1)
        self.merged - dataframe with userID, movieID, updaterating, genre 
        self.genres - array with name genres 
        self.users_id - array with all user_id 
        self.mean_genres - dict with rating for all genres 
        self.dataframe_with_mean - dataframe with userID and rating for all genres 

        """
        self.file_name_1 = "../user_ratedmovies.dat"
        self.file_name_2 = "../movie_genres.dat"
        self.df, self.merged, self.genres, self.users_id = join_dataframe(self.file_name_1, self.file_name_2)
        self.mean_genres = self.create_or_update_mean_genres() #update merged 
        self.dataframe_with_mean = self.create_or_update_matrix()
    
    def create_or_update_matrix(self):
        return create_matrix_all_user(self.users_id, self.genres,self.merged, self.mean_genres)

    def create_or_update_mean_genres(self):
        return get_mean_of_all_genres(self.df, self.merged) #update merged 

    def add_new_profile(self,new_user_id,new_profile):
        new_profile['userID'] = new_user_id 
        self.dataframe_with_mean = self.dataframe_with_mean.append(new_profile, ignore_index=True)
        self.all_update()

    def all_update(self, ): 
        self.update_user_id()
        self.mean_genres = self.create_or_update_mean_genres()
        self.dataframe_with_mean = self.create_or_update_matrix()

    def add_new_rows_to_merged(self, row):
        genres = []
        print("ROWOWOWOWOWOWOWOOWOWO")
        #print(row)
        # for k,v in row.items():
        #     if k !="userID" and k!= "movieID" and k!="rating":
        #         if v==1:
        #             genres.append(k)
        
        # rows_to_merged = []
   
        # for genre in genres:
        #     row_to_merged = {
        #     "userID" : row['userID'], 
        #     "movieID" : row["movieID"], 
        #     "rating" : row["rating"]
        #     }
        #     row_to_merged["genre"] = genre
            
        #     rows_to_merged.append(row_to_merged)
        # df = pd.DataFrame(rows_to_merged)
        # self.merged = self.merged.append(df, sort=False, ignore_index=True)
      


    def add_new_rating(self,row):
        #row -> userID, movieID, rating, genres -> 0,1 
        self.df = self.df.append(row, ignore_index=True)
        self.add_new_rows_to_merged(row)
        self.all_update()
    
    def update_genres(self, new_genre):
        self.genres.append(new_genre)

    def update_user_id(self):
        self.user_id = self.dataframe_with_mean['userID'].unique()

    def show_all_ratings(self):
        return DataFrame_to_dict(self.dataframe_with_mean)

    def del_row_from_data(self, id):
        index = self.data.dataframe_with_mean[self.dataframe_with_mean['userID']==id].tolist()[0]
        self.dataframe_with_mean = self.dataframe_with_mean.drop(self.dataframe_with_mean.index[index])

    def get_mean_for_all_user_all_genres(self):
        return self.mean_genres


    def show_rating_for_user(self, id):
        result = self.dataframe_with_mean[self.dataframe_with_mean['userID']==id]
        return result.to_dict(orient='records')





if __name__ == '__main__':
    api = ApiLogic()
    print(api.df.head())
    print(api.merged.head())
    print(api.dataframe_with_mean.head())
    # print(api.dataframe_with_mean.head())
    row = {"userID": 78, "movieID": 903, "rating": 4.0, "Action": 0, "Adventure": 0, "Animation": 0, "Children": 0,
"Comedy": 0, "Crime": 0, "Documentary": 0, "Drama": 1, "Fantasy": 0, "Film-Noir": 0, "Horror": 0,
"IMAX": 0, "Musical": 0, "Mystery": 1, "Romance": 1, "Sci-Fi": 0, "Short": 0, "Thriller": 1, "War":
0, "Western": 0}
    # print(api.merged.tail(20))
    # api.add_new_rating(row)
    # print(api.merged.tail(20))
    api.show_rating_for_user(75)



