from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.models import User

from apps.movies.api.serializers import MovieSerializer
from apps.movies.forms import UserForm, MoviesForm, RatingMoviesForm, UserTokenForm, QueryMovieForm
from apps.movies.models import Movie, MovieRate, UserToken
from django.conf import settings
from django.shortcuts import resolve_url
from django.core.management import call_command
from django.contrib.auth import logout as auth_logout
from rest_framework.renderers import JSONRenderer


class Index(ListView):
    template_name = 'index.html'
    queryset = Movie.objects.all()
    paginate_by = 5

    def get_queryset(self):
        qs = super(Index, self).get_queryset()
        return qs.order_by('-id')


class SignUp(CreateView):
    model = User
    template_name = 'index.html'
    form_class = UserForm
    success_url = reverse_lazy('index')


class RegisterMovie(LoginRequiredMixin, CreateView):
    model = Movie
    template_name = 'register_movie.html'
    form_class = MoviesForm
    success_url = reverse_lazy('index')


class MovieList(LoginRequiredMixin, ListView):
    template_name = 'list_movie.html'
    queryset = Movie.objects.all()

    def get_queryset(self):
        qs = super(MovieList, self).get_queryset()
        return qs.order_by('-id')


class MovieUpdate(LoginRequiredMixin, UpdateView):
    model = Movie
    template_name = 'register_movie.html'
    form_class = MoviesForm
    success_url = reverse_lazy('index')


class MovieDelete(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'delete_movie.html'
    success_url = reverse_lazy('movie_list')


class MovieDetail(DetailView):
    model = Movie
    template_name = 'detail_movie.html'
    second_form_class = RatingMoviesForm
    slug_field = 'slug'
    query_pk_and_slug = False

    def get_context_data(self, **kwargs):
        context = super(MovieDetail, self).get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context


class RegisterMovieRating(LoginRequiredMixin, CreateView):
    model = MovieRate
    template_name = 'rating_movie.html'
    form_class = RatingMoviesForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LoginViewModified(LoginView):
    form_class_second = UserTokenForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = User.objects.get(username=request.POST.get('username'))
        form_second = self.form_class_second()
        if form.is_valid():
            try:
                UserToken.objects.get(user=user)
            except Exception:
                data = form_second.save(commit=False)
                data.user = user
                data.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutViewModified(LogoutView):
    form_class_second = UserTokenForm

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user)
            form_second = self.form_class_second()
            try:
                erase = UserToken.objects.get(user=user).delete()
                data = form_second.save(commit=False)
                data.erase.delete()
                data.save()
            except Exception:
                pass
        except Exception:
            return self.get(request, *args, **kwargs)

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)
        auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)


def logout_then_login_modified(request, login_url=None):
    login_url = resolve_url(login_url or settings.LOGIN_URL)
    return LogoutViewModified.as_view(next_page=login_url)(request)


class QueryMovieView(FormView):
    template_name = 'query_movies.html'
    form_class = QueryMovieForm
    success_url = reverse_lazy('movie_list')

    def form_valid(self, form):
        data = form.cleaned_data['query']
        call_command('download', '-s', data)
        return super().form_valid(form)


class MovieListView(ListView):
    model = Movie
    content_type = 'application/json'
    response_class = HttpResponse

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'serializer_data': JSONRenderer().render(MovieSerializer(self.get_queryset(), many=True).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(context.get('serializer_data'), **response_kwargs)


class MovieDetailView(DetailView):
    model = Movie
    content_type = 'application/json'
    response_class = HttpResponse
    slug_field = 'slug'
    query_pk_and_slug = False

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
        context.update({'serializer_data': JSONRenderer().render(MovieSerializer(self.object).data)})
        return super().get_context_data(**context)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(context.get('serializer_data'), **response_kwargs)
