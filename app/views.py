import pandas as pd
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from app.models import Mileage, Branch, Series
from app.serializers import ReportDataSerializer
from core.db_utils import engine
from core.mixins import LoggerMixin


def index_page(request):
    return render(request, "index.html")


@api_view(http_method_names=['GET'])
def get_period_range(request):
    filter_params = dict()
    from_date = request.query_params.get('from') if request.query_params.get('from') not in ['-', 'null'] else None
    to_date = request.query_params.get('to') if request.query_params.get('to') not in ['-', 'null'] else None
    if from_date:
        filter_params.update(
            {
                'year__gte': int(from_date)
            }
        )
    if to_date:
        filter_params.update(
            {
                'year__lte': int(to_date)
            }
        )
    periods = list(Mileage.objects.filter(**filter_params).values_list('year', flat=True).distinct('year'))
    return Response(periods)


@api_view(http_method_names=['GET'])
def get_branches(request):
    branches = Branch.objects.values_list('name', flat=True)
    return Response(branches)


@api_view(http_method_names=['GET'])
def get_series(request):
    branches_names = request.query_params.get('branches') if request.query_params.get('branches') != 'null' else None
    if branches_names:
        branches_names = branches_names.split(',')
        series = Mileage.objects.filter(branch__name__in=branches_names).values_list('series__name', flat=True).distinct('series__name')
    else:
        series = Series.objects.values_list('name', flat=True)
    return Response(series)


class ReportData(ListAPIView,
                 LoggerMixin):
    serializer_class = ReportDataSerializer
    ordering = ['year', ]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        from_year = query_params.get('from_year')
        to_year = query_params.get('to_year')
        branches = query_params.get('branches')
        series = query_params.get('series')
        if from_year and from_year != 'null':
            queryset = queryset[queryset.year >= int(from_year)]
        if to_year and to_year != 'null':
            queryset = queryset[queryset.year <= int(to_year)]
        if branches and branches != 'null':
            branches = branches.split(',')
            queryset = queryset[queryset.branch_name.isin(branches)]
        if series and series != 'null':
            series = series.split(',')
            queryset = queryset[queryset.series_name.isin(series)]
        self.logger.info(queryset)
        queryset = queryset.pivot_table(['total_cost'], ['year'], aggfunc='sum')
        self.logger.info(queryset)
        if not queryset.empty:
            queryset = [{'year': year, 'total_cost': queryset.total_cost[year]} for year in queryset.total_cost.index]
        self.logger.info(queryset)
        return queryset

    def get_queryset(self):
        query = '''
        select
            branch.name as branch_name,
            series.name as series_name,
            series.value as cost,
            mileage.value as mileage_value,
            mileage.year as year
        from app_mileage mileage
        join app_series series on mileage.series_id = series.id
        join app_branch branch on mileage.branch_id = branch.id
        '''
        pd_engine = engine()
        report = pd.read_sql_query(query, pd_engine)
        pd_engine.dispose()
        report['total_cost'] = report['mileage_value'] * report['cost'] / 1000000
        self.logger.info(report)
        return report
