from django.urls import path

from app.views import ReportData, get_period_range, get_branches, get_series

urlpatterns = [
    path('report_data/', ReportData.as_view(), name='report_data'),
    path('common/year_range/', get_period_range, name='year_range'),
    path('common/branches/', get_branches, name='branches'),
    path('common/series/', get_series, name='series'),
]
