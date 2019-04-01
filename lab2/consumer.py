from queueRedis import QueueRedis
import json
import pandas as pd


class Consumer:

    def __init__(self):
        self.qr = QueueRedis()
        self.name = "queue_to_write"
        self.batch = 0
        self.done = True
        self.df = pd.DataFrame()



    def get_data(self):
        """
        Getting/Reading batch of data from queue.
        Triming queue.
        :return: reading data
        """
        try:
            result = self.qr._get(self.name, 0, self.batch)
        except:
            result = self.qr._get(self.name)

        self.qr._trim(self.name, len(result), -1) #trim queue
        print("triming")
        return result

    def show_data(self):
        """
        Print reading data
        :return:
        """
        result = c.get_data()
        if len(result) == 0:
            self.done = False
        else:
            res = self.qr._load_data(result[0])
            #self.df.append(res)
            print(res)









if __name__== "__main__":
    c = Consumer()
    while c.done:
        c.show_data()
