import requests
import json
from databricks.sdk.runtime import dbutils


API_KEY = dbutils.secrets.get(catalog = 'films', schema="config",key='tmdb_api_key')

URL_MOVIE_INFO = "https://api.themoviedb.org/3/movie/{movie_id}"
URL_SERIE_INFO = "https://api.themoviedb.org/3/tv/{serie_id}"
URL_MOVIE_CREW = "https://api.themoviedb.org/3/movie/{movie_id}/credits"
URL_SERIE_CREW = "https://api.themoviedb.org/3/tv/{serie_id}/credits"
URL_PERSON = "https://api.themoviedb.org/3/person/{person_id}"
URL_MOVIE_KEYWORDS = "https://api.themoviedb.org/3/movie/{movie_id}/keywords"
URL_SERIE_KEYWORDS = "https://api.themoviedb.org/3/tv/{serie_id}/keywords"
URL_MOVIE_IMAGE = "https://api.themoviedb.org/3/movie/{movie_id}/images"
URL_SERIE_IMAGE = "https://api.themoviedb.org/3/tv/{serie_id}/images"

path = "/Volumes/films/bronze/landing/TMDB/"
path_movie          = path + "Film/{id}.json"
path_serie          = path + "Série/{id}.json"
path_movie_crew     = path + "Film_crew/{id}.json"
path_serie_crew     = path + "Série_crew/{id}.json"
path_movie_image    = path + "Film_images/{id}.json"
path_serie_image    = path + "Série_images/{id}.json"
path_movie_keywords = path + "Film_keywords/{id}.json"
path_serie_keywords = path + "Série_keywords/{id}.json"
path_person         = path +"person/{id}.json"
headers = {
    "accept" : "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

session = requests.Session()
session.headers.update(headers)



def download_info(id,type):
    if id == -1 : return print("Film absent sur TMDB")
    if type == 'Film':
        url_info = URL_MOVIE_INFO.format(movie_id=id)
        url_crew = URL_MOVIE_CREW.format(movie_id=id)
        url_image = URL_MOVIE_IMAGE.format(movie_id=id)
        url_keywords = URL_MOVIE_KEYWORDS.format(movie_id=id)

    if type == 'Série':
        url_info = URL_SERIE_INFO.format(serie_id=id)
        url_crew = URL_SERIE_CREW.format(serie_id=id)
        url_image = URL_SERIE_IMAGE.format(serie_id=id)
        url_keywords = URL_SERIE_KEYWORDS.format(serie_id=id)
        

    response_info = session.get(url_info).json()
    response_crew = session.get(url_crew).json()
    response_image = session.get(url_image).json()
    response_keywords = session.get(url_keywords).json()


    if type == 'Film':
        dbutils.fs.put(path_movie.format(id=id), json.dumps(response_info), overwrite=True)
        dbutils.fs.put(path_movie_crew.format(id=id), json.dumps(response_crew), overwrite=True)
        dbutils.fs.put(path_movie_image.format(id=id), json.dumps(response_image), overwrite=True)
        dbutils.fs.put(path_movie_keywords.format(id=id), json.dumps(response_keywords), overwrite=True)
    if type == 'Série':
        dbutils.fs.put(path_serie.format(id=id), json.dumps(response_info), overwrite=True)
        dbutils.fs.put(path_serie_crew.format(id=id), json.dumps(response_crew), overwrite=True)
        dbutils.fs.put(path_serie_image.format(id=id), json.dumps(response_image), overwrite=True)
        dbutils.fs.put(path_serie_keywords.format(id=id), json.dumps(response_keywords), overwrite=True)



def download_person(id):
    url_person = URL_PERSON.format(person_id=id)
    response_person = session.get(url_person).json()
    dbutils.fs.put(path_person.format(id=id), json.dumps(response_person), overwrite=True)