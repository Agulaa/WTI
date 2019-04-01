import redis
import json
import pandas as pd
class QueueRedis:

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6381, db=0)

    def _add(self, name, value):
        """
        Add to queue or extend value
        :param name: name queue
        :param value: value to add to queue
        """
        return self.r.rpush(name, value)

    def _get(self, name, start=0, stop=-1):
        """
        Returns the specified elements of the list stored at name.
        :param name: name queue
        :param start: start of range
        :param stop: stop of range
        :return:
        """
        return self.r.lrange(name, start, stop)

    def _flushdb(self):
        """
        Delete all the keys of the currently selected DB
        :return: empty db
        """
        return self.r.flushdb()

    def _trim(self, name, start=0, stop=-1):
        """
        Trim an existing list, it will contain only the specified range
        :param key:
        :param start:
        :param stop:
        :return:
        """
        return self.r.ltrim(name, start, stop)

    def _load_data(self,_json):
        """
        Loads json
        :param _json:
        :return:
        """
        result = json.loads(_json)
        return result


    def _print_data(self, dic):
        """

        :param dic:
        :return:
        """
        for k, v in dic.items():
            print(k, ":", v)

    def _prepare_data(self, dic):
        """

        :param dic:
        :return:
        """
        value = json.dumps(dic)
        return value

    def _random_dic(self):
        """
        Make random json
        :return: json
        """
        date = {}
        for i in range(10):
            date[i] = f"message {i}"
        return date







if __name__=="__main__":
    qr = QueueRedis()
    qr._load_data_from_file()