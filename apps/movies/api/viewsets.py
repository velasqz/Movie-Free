from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.movies.api.serializers import MovieSerializer, MovieRateSerializer, MovieSerializer2
from apps.movies.models import Movie, MovieRate


class ExampleViewset(viewsets.ViewSet):

    def list(self, request):
        return Response({'Action': 'List'})

    def retrieve(self, request, pk=None):
        return Response({'Action': 'Retrieve'})

    def create(self, request):
        return Response({'Action': 'Create'})

    def update(self, request, pk=None):
        return Response({'Action': 'Update'})

    def destroy(self, request, pk=None):
        return Response({'Action': 'Destroy'})


class MovieDetailView2(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class MovieRateListView(ListAPIView):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class MovieRateDetailView(RetrieveAPIView):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class MovieListCreateView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer2


class MovieRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer2


class CreateListRetrieveUpdateDestroyViewSet(mixins.CreateModelMixin,
                                             mixins.ListModelMixin,
                                             mixins.RetrieveModelMixin,
                                             mixins.DestroyModelMixin,
                                             mixins.UpdateModelMixin,
                                             viewsets.GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer2
