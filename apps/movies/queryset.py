from django.db.models import QuerySet, Sum, Count, FloatField


class MovieRateQueryset(QuerySet):
    def get_best_rated(self):
        return self.values('movie').annotate(
            rate=Sum('rating', output_field=FloatField()) / Count('movie', output_field=FloatField())).order_by(
            '-rating')
