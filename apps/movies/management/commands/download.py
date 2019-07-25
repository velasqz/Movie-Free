import requests
from django.core.management.base import BaseCommand
from apps.movies.models import Movie, Language, MovieDirector, MovieActor, Country
from datetime import datetime


class Command(BaseCommand):
    help = 'fetch movies from OMDB API'

    def add_arguments(self, parser):
        # positional argument
        parser.add_argument('title', type=str)

        # kwargs like arguments
        parser.add_argument('-s', '--search', action='store_true', default=False)

    def handle(self, *args, **options):
        search = options['search']
        title = options['title']

        if search == True:
            response = requests.get(
                'http://www.omdbapi.com/?s={}&plot=full&apikey=7225a9db&type=movie'.format(title)).json()
            try:

                for data in response['Search']:
                    sub_response = requests.get(
                        'http://www.omdbapi.com/?i={}&plot=full&apikey=7225a9db&type=movie'.format(
                            data['imdbID'])).json()

                    rang_lan = sub_response['Language'].replace(', ', ',').split(',')
                    rang_act = sub_response['Actors'].replace(', ', ',').split(',')
                    rang_dir = sub_response['Director'].replace(', ', ',').split(',')
                    rang_cou = sub_response['Country'].replace(', ', ',').split(',')

                    for lan in rang_lan:
                        Language.objects.get_or_create(name=lan, defaults={'name': lan})

                    for actor in rang_act:
                        MovieActor.objects.get_or_create(name=actor, defaults={'name': actor, 'age': 21})

                    for director in rang_dir:
                        MovieDirector.objects.get_or_create(name=director, defaults={'name': director, 'age': 21})

                    for countr in rang_cou:
                        Country.objects.get_or_create(name=countr, defaults={'name': countr})

                    try:
                        try:
                            release_date = sub_response['Released']
                            release_date = release_date.replace(' ', '-')
                            release_date = datetime.strptime(release_date, '%d-%b-%Y')
                        except Exception:
                            release_date = None

                        try:
                            response = requests.get(sub_response['Poster'])
                            f = open('media/movie/{}.{}'.format(sub_response['Title'],
                                                                sub_response['Poster'].split('.')[-1]), 'wb')
                            f.write(response.content)
                            f.close()
                            poster = 'movie/{}.{}'.format(sub_response['Title'],
                                                          sub_response['Poster'].split('.')[-1])
                        except Exception:
                            poster = 'movie/{}.{}'.format('NA', '.jpg')

                        title = sub_response['Title']
                        genre = sub_response['Genre'].replace(', ', ',').split(',')[0]
                        duration = 0 if sub_response['Runtime'].split(' ')[0] == 'N/A' else \
                            sub_response['Runtime'].split(' ')[0]
                        detail = None if sub_response['Plot'] == 'N/A' else sub_response['Plot']
                        original_language = Language.objects.get(name=rang_lan[0])
                        country = Country.objects.get(name=rang_cou[0])
                        movie, _ = Movie.objects.update_or_create(title=title,
                                                                  defaults={'title': title,
                                                                            'release_date': release_date,
                                                                            'duration': duration,
                                                                            'genre': genre, 'detail': detail,
                                                                            'original_language': original_language,
                                                                            'country': country, 'poster': poster})

                        for actor in rang_act:
                            movie.actors.add(MovieActor.objects.get(name=actor))

                        for director in rang_dir:
                            movie.directors.add(MovieDirector.objects.get(name=director))

                        print('movie added')
                    except Exception as e:
                        print('movie not added, Exception: {}'.format(str(e)))

            except Exception as e:
                print('Url does not validate'.format(str(e)))
