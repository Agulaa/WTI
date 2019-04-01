from queueRedis import QueueRedis
import json
import time
import pandas as pd

class Producer:

    def __init__(self):
        self.qr = QueueRedis()
        self.name = "queue_to_write"
        self.data = self._load_data_from_file()
        self.row_iterrator = self.data.iterrows()
        self.last_elem = self.data.shape[0]
        self.NotDone = True
        self.row_id = 0


    def _load_data_from_file(self):
        """
        Loading data from file - user_ratedmovies.dat
        :return: DataFrame
        """
        data = pd.read_csv("../user_ratedmovies.dat", sep="\t", usecols=["userID", "movieID", "rating"])
        return data


    def add_to_queue(self):
        """
        Adding dic to queue
        :return:
        """
        dic = self.qr._random_dic()
        value = self.qr._prepare_data(dic)
        self.qr._add(self.name, value)

    def change_rows_to_dic(self, row):
        """
        Changing rows to dic - its important because next
        will be change dic to json
        :param row: row from data frame
        :return: dictionary with data from row
        """
        return self.data.iloc[row].to_dict()

    def send_data(self, n):
        """
        Adding dic with data from row to queue.
        Adding specifiy diagnostic id to dic
        If iterrator will be on the last element - change flag NotDone
        :param n: number of row to send
        """
        #row_id = 0
        for r, _ in zip(self.row_iterrator, range(0,n)):
            dict_to_send = self.change_rows_to_dic(r[0])
            dict_to_send["diagnostic_id"] = self.row_id
            value = self.qr._prepare_data(dict_to_send)
            self.qr._add(self.name, value)
            self.row_id+=1
            if r[0] == self.last_elem:
                self.NotDone = False





if __name__ == '__main__':
    p = Producer()
    #p.qr._flushdb()
    p._load_data_from_file()
    for i in range(5):
        p.send_data(10)
        time.sleep(10)
        print("send")
    # # while p.NotDone:
    #     p.send_data(100)
    #     time.sleep(100)






