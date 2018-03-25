from rest_framework import serializers


class ReportDataSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    total_cost = serializers.FloatField()
