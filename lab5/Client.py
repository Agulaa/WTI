import requests


class Client:

    def request_get(self, url):
        r = requests.get(url)
        print("request url", r.url)
        print("request status code", r.status_code)
        print("request text", r.text)
        print("request headers",r.headers)
        print("request request.headers",r.request.headers)

    def request_post(self, url, payload):

        r = requests.post(url, params=payload)
        print("request url", r.url)
        print("request status code", r.status_code)
        #print("request text", r.text)
        print("request headers",r.headers)
        print("request request.headers",r.request.headers)


    def request_delete(self, url):

        r = requests.delete(url)

        print("request url", r.url)
        print("request status code", r.status_code)
        #print("request text", r.text)
        print("request headers",r.headers)
        print("request request.headers",r.request.headers)



if __name__=='__main__':
    c = Client()
    # print("----------------------------------------------------------")
    # c.request_get('http://127.0.0.1:5000/ratings')
    # print("----------------------------------------------------------")
    # c.request_get('http://127.0.0.1:5000/avg-genre-ratings/all-users')
    # print("----------------------------------------------------------")
    # c.request_get('http://127.0.0.1:5000/avg-genre-ratings/78')
    # print("----------------------------------------------------------")


    payload =  {"userID": 78, "movieID": 903, "rating": 4.0, "Action": 0, "Adventure": 0, "Animation": 0, "Children": 0,
"Comedy": 0, "Crime": 0, "Documentary": 0, "Drama": 1, "Fantasy": 0, "Film-Noir": 0, "Horror": 0,
"IMAX": 0, "Musical": 0, "Mystery": 1, "Romance": 1, "Sci-Fi": 0, "Short": 0, "Thriller": 1, "War":
0, "Western": 0}
    c.request_post('http://127.0.0.1:5000/rating', payload)

   # c.request_delete('http://127.0.0.1:5000/delete/rating')

