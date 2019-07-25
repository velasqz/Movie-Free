from django.urls import path

from apps.movies.views import SignUp, RegisterMovie, Index, MovieList, MovieUpdate, MovieDelete, MovieDetail, \
    RegisterMovieRating, LoginViewModified, logout_then_login_modified, QueryMovieView, MovieDetailView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/login', LoginViewModified.as_view(template_name='index.html'), name="login"),
    path('logout', logout_then_login_modified, name='logout'),
    path('register_user', SignUp.as_view(), name='register_user'),
    path('register_movie', RegisterMovie.as_view(), name='register_movie'),
    path('movie_list', MovieList.as_view(), name='movie_list'),
    path('movie_update/<slug>/', MovieUpdate.as_view(), name='movie_update'),
    path('movie_delete/<slug>/', MovieDelete.as_view(), name='movie_delete'),
    path('movie_detail/<slug>/', MovieDetail.as_view(), name='movie_detail'),
    path('register_rating', RegisterMovieRating.as_view(), name='register_rating'),
    path('query_movie', QueryMovieView.as_view(), name='query_movie'),
    path('movie_detail_view/<slug>/', MovieDetailView.as_view(), name='movie_detail_view'),
]
