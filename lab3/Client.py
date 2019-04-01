import requests


class Client:

    def request_get(self, url):
        r = requests.get(url)
        print(r.url)
        print(r.status_code)
        print(r.text)
        print(r.headers)


    def request_post(self, url, payload):

        r = requests.post(url, params=payload)

        print(r.url)
        print(r.status_code)
        print(r.text)
        print(r.headers)

    def request_delete(self, url):

        r = requests.delete(url)

        print(r.url)
        print(r.status_code)
        print(r.text)
        print(r.headers)


if __name__=='__main__':
    c = Client()
    c.request_get('http://127.0.0.1:5000/ratings')
    c.request_get('http://127.0.0.1:5000/avg-genre-ratings/all-users')
    c.request_get('http://127.0.0.1:5000/avg-genre-ratings/75')


    payload = {"userID": 78, "movieID": 903, "rating": 4.0, "genre-Action": 0, "genre-Adventure": 0, "genre-Animation": 0,
    "genre-Children": 0, "genre-Comedy": 0, "genre-Crime": 0, "genre-Documentary": 0, "genre-Drama": 1,
    "genre-Fantasy": 0, "genre-Film-Noir": 0, "genre-Horror": 0, "genre-IMAX": 0, "genre-Musical": 0,
    "genre-Mystery": 1, "genre-Romance": 1, "genre-Sci-Fi": 0, "genre-Short": 0, "genre-Thriller": 1, "genre-War":
    0, "genre-Western": 0}
    c.request_post('http://127.0.0.1:5000/rating', payload)

    c.request_delete('http://127.0.0.1:5000/delete/rating')

