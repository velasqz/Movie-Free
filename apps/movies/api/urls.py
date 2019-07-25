from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.movies.api.viewsets import CreateListRetrieveUpdateDestroyViewSet, MovieDetailView2, MovieRateListView, \
    MovieRateDetailView, MovieListCreateView, MovieRetrieveUpdateDestroyView

router = DefaultRouter()
router.register('movie/v2', CreateListRetrieveUpdateDestroyViewSet)

urlpatterns = [
    path('movie_detail_view2/<slug>/', MovieDetailView2.as_view(), name='movie_detail_view2'),
    path('movie_rate_list_view', MovieRateListView.as_view(), name='movie_rate_list_view'),
    path('movie_rate_detail_view/<int:pk>/', MovieRateDetailView.as_view(), name='movie_rate_detail_view'),

    path('movie/v1/', MovieListCreateView.as_view(), name='list_create'),
    path('movie/v1/<int:pk>', MovieRetrieveUpdateDestroyView.as_view(), name='update_destroy_detail'),

    path('', include(router.urls)),

    path('movie/v3/', CreateListRetrieveUpdateDestroyViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='movie-list-actions'),
    path('movie/v3/<int:pk>/',
         CreateListRetrieveUpdateDestroyViewSet.as_view(
             {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='movie-detail-actions'),
]
