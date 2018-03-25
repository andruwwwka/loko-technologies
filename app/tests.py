from django.test import TransactionTestCase, TestCase
from django.urls import reverse

from app.models import Branch, Series


class TestApplicationResourcesAvailable(TestCase):

    def test_main_page_is_available(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_report_data_is_available(self):
        response = self.client.get(reverse('report_data'))
        self.assertEqual(response.status_code, 200)

    def test_year_range_is_available(self):
        response = self.client.get(reverse('year_range'))
        self.assertEqual(response.status_code, 200)

    def test_branches_is_available(self):
        response = self.client.get(reverse('branches'))
        self.assertEqual(response.status_code, 200)

    def test_series_is_available(self):
        response = self.client.get(reverse('series'))
        self.assertEqual(response.status_code, 200)


class TestReportDataResource(TransactionTestCase):

    fixtures = ['fixtures/data.json', ]

    def setUp(self):
        super().setUp()
        self.series = Series.objects.values_list('name', flat=True)
        self.branches = Branch.objects.values_list('name', flat=True)

    def test_without_filters(self):
        response = self.client.get(reverse('report_data'))
        years = [int(item.get('year')) for item in response.data]
        min_year = min(years)
        max_year = max(years)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(min_year, 2017)
        self.assertEqual(max_year, 2054)

    def test_min_year_filter(self):
        response = self.client.get(
            reverse('report_data'),
            {'from_year': 2030}
        )
        years = [int(item.get('year')) for item in response.data]
        min_year = min(years)
        max_year = max(years)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(min_year, 2030)
        self.assertEqual(max_year, 2054)

    def test_max_year_filter(self):
        response = self.client.get(
            reverse('report_data'),
            {'to_year': 2040}
        )
        years = [int(item.get('year')) for item in response.data]
        min_year = min(years)
        max_year = max(years)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(min_year, 2017)
        self.assertEqual(max_year, 2040)

    def test_branches_filter(self):
        response1 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'branches': self.branches[0]
            }
        )
        response2 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'branches': self.branches[1]
            }
        )
        response3 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'branches': "{},{}".format(self.branches[0], self.branches[1])
            }
        )
        sum_resp3 = sum([item['total_cost'] for item in response3.data])
        sum_resp1_and_resp2 = sum(
            [item['total_cost'] for item in response1.data] +
            [item['total_cost'] for item in response2.data]
        )
        self.assertGreater(sum_resp3, 0)
        self.assertAlmostEqual(sum_resp3, sum_resp1_and_resp2)

    def test_series_filters(self):

        response1 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'series': self.series[10]
            }
        )
        response2 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'series': self.series[6]
            }
        )
        response3 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'series': "{},{}".format(self.series[6], self.series[10])
            }
        )
        sum_resp3 = sum([item['total_cost'] for item in response3.data])
        sum_resp1_and_resp2 = sum(
            [item['total_cost'] for item in response1.data] +
            [item['total_cost'] for item in response2.data]
        )
        self.assertGreater(sum_resp3, 0)
        self.assertAlmostEqual(sum_resp3, sum_resp1_and_resp2)

    def test_all_filters(self):
        branches = Branch.objects.all()
        branch1 = branches[1]
        branch2 = branches[5]
        series_for_branch1 = branch1.branch_mileage.all().values_list('series__name', flat=True).distinct('series__name')
        series_for_branch2 = branch2.branch_mileage.all().values_list('series__name', flat=True).distinct('series__name')
        response1 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'series': '{},{},{},{}'.format(
                    series_for_branch1[1],
                    series_for_branch1[3],
                    series_for_branch2[1],
                    series_for_branch2[3]),
                'branches': branch1.name,
            }
        )
        response2 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'series': '{},{},{},{}'.format(
                    series_for_branch1[1],
                    series_for_branch1[3],
                    series_for_branch2[1],
                    series_for_branch2[3]),
                'branches': branch2.name,
            }
        )
        response3 = self.client.get(
            reverse('report_data'),
            {
                'from_year': 2020,
                'to_year': 2040,
                'series': '{},{},{},{}'.format(
                    series_for_branch1[1],
                    series_for_branch1[3],
                    series_for_branch2[1],
                    series_for_branch2[3]),
                'branches': '{},{}'.format(branch1.name, branch2.name)
            }
        )
        sum_resp3 = sum([item['total_cost'] for item in response3.data])
        sum_resp1_and_resp2 = sum(
            [item['total_cost'] for item in response1.data] +
            [item['total_cost'] for item in response2.data]
        )
        self.assertGreater(sum_resp3, 0)
        self.assertAlmostEqual(sum_resp3, sum_resp1_and_resp2)
