import pandas as pd
import requests
from IPython.display import display,Image,clear_output
from databricks.sdk.runtime import dbutils

API_KEY =  dbutils.secrets.get(catalog="films", schema="config", key="tmdb_api_key")
URL_MOVIE_SEARCH = "https://api.themoviedb.org/3/search/movie"
URL_TV_SEARCH = "https://api.themoviedb.org/3/search/tv"
URL_IMAGE = "https://image.tmdb.org/t/p/w500"

PATH_MAPPING = '/Volumes/films/bronze/landing/mapping/mapping_tmdb.csv'
PATH_SCORES = '/Volumes/films/bronze/landing/sheet/scores.csv'

headers = {
    "accept" : "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def find_id_movie(titres):
    for movie_title in titres:
        type_show = "Film"
        id = check_id_tmdb(movie_title, "Film")
        if id == "SERIE":
            type_show = "Série"
            id = check_id_tmdb(movie_title, "Série")

        if id == "STOP":
            print(f"Petite pause ! On s'arrête au titre {movie_title}")
            break

        if id is None or id == 'vide':
            print(f"{movie_title} n'a pas réussi à s'associer, le faire manuellement")
            ligne = pd.DataFrame([[movie_title,-1, type_show]],columns=["Titre","id","Type"])

        else:
            print(f"{movie_title} est associé à l'id : {id}")
            ligne = pd.DataFrame([[movie_title,id, type_show]],columns=["Titre","id","Type"])

        mapping = pd.read_csv(PATH_MAPPING)
        mapping = pd.concat([mapping, ligne], ignore_index=True)
        mapping.to_csv(PATH_MAPPING, index=False)


def check_id_tmdb(title, type_show):
    params = {
        "query": title,
        "language": "en-US"
    }

    if type_show == "Film":
        response = requests.get(URL_MOVIE_SEARCH, params=params, headers=headers, timeout=10)
        name_col = "title"
    else:
        response = requests.get(URL_TV_SEARCH, params=params, headers=headers, timeout=10)
        name_col = "name"
    response.raise_for_status()

    data = response.json()
    if not data["results"]:
        print(f"Aucun résultat pour '{title}'")
        return None

    df = pd.DataFrame(data["results"])
    df_image = df["poster_path"].dropna()

    for image in df_image:
        print(f"Le titre à chercher est {title}")
        display(df[[name_col, "popularity", "vote_average", "vote_count"]][df["poster_path"] == image])
        display(Image(URL_IMAGE + image))

        choix = input(f"Is it this {type_show} ? (Y/N/vide/stop/serie)")
        clear_output(wait=True)
        if choix == 'Y':
            return df["id"][df["poster_path"] == image].iloc[0]
        if choix != 'N':
            return choix