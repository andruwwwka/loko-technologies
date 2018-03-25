import xlrd
from django.core.management.base import BaseCommand
from django.db import transaction

from app.models import Branch, Series, Mileage
from core.mixins import LoggerMixin


class Command(BaseCommand,
              LoggerMixin):
    help = 'Заполнение таблиц начальными данными'

    def fill_branches(self, book):
        self.logger.info('Запуск заполнения таблицы филиалов')
        if not Branch.objects.exists():
            branch_sheet = book.sheet_by_name('Филиал')
            for row in branch_sheet.col_values(0):
                Branch.objects.create(
                    name=row
                )
                self.logger.info('Добавлена запись филиала: {}'.format(row))
        else:
            self.logger.info('Таблица филиалов уже заполнена')

    def fill_series(self, book):
        self.logger.info('Запуск заполнения таблицы локомотивов')
        if not Series.objects.exists():
            series_sheet = book.sheet_by_name('Ставка за км')
            for row_index in range(1, series_sheet.nrows):
                series, cost = series_sheet.row_values(row_index)
                Series.objects.create(
                    name=series,
                    value=cost
                )
                self.logger.info('Добавлена запись локомотива: {}({})'.format(series, cost))
        else:
            self.logger.info('Таблица локомотивов уже заполнена')

    def fill_mileage(self, book):
        self.logger.info('Запуск заполнения таблицы пробега')
        if not Mileage.objects.exists():
            mileage_sheet = book.sheet_by_name('Пробег')
            header = mileage_sheet.row_values(0)
            for row_index in range(1, mileage_sheet.nrows):
                row = mileage_sheet.row_values(row_index)
                branch_name = row[0]
                series_name = row[1]
                series = Series.objects.get(name=series_name)
                branch = Branch.objects.get(name=branch_name)
                for year_index in range(2, len(row)):
                    year = int(header[year_index])
                    value = int(round(row[year_index]))
                    Mileage.objects.create(
                        branch=branch,
                        series=series,
                        year=year,
                        value=value
                    )
                    self.logger.info(
                        'Добавлена запись пробега: {}-{}-{}-{}'.format(branch_name, series_name, year, value))
        else:
            self.logger.info('Таблица пробега уже заполнена')

    @transaction.atomic
    def handle(self, *args, **options):
        worlbook = xlrd.open_workbook('test_LT.xlsx')
        print(worlbook.sheet_names())
        self.fill_branches(worlbook)
        self.fill_series(worlbook)
        self.fill_mileage(worlbook)
