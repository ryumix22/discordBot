import os
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from pprint import pprint
import kinopoisk_unofficial.response.films.film_response as resp


# kpAPIKey = os.getenv('KINOPOISKAPIKEY')
# apiClient = KinopoiskApiClient(kpAPIKey)
apiClient = KinopoiskApiClient('a0ce66c9-347f-478e-a996-cf28bc2c774c')


def getFilmByName(name: str):
    request = SearchByKeywordRequest(name)
    response = apiClient.films.send_search_by_keyword_request(request)
    pprint(response.films[0])
    request = FilmRequest(response.films[0].film_id)
    response = apiClient.films.send_film_request(request)
    film = resp.unwrap_film(response)
    pprint(resp.unwrap_film(response))
    pprint(film.name_ru)
    return film


def getListOfGenres(id):
    request = FilmRequest(id)
    response = apiClient.films.send_film_request(request)
    film = resp.unwrap_film(response)
    listOfGenres = film.genres
    retArr = []
    for genre in listOfGenres:
        retArr.append(genre.genre)
    return retArr
