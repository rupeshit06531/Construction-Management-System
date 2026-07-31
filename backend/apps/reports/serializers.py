from rest_framework import serializers


class ReportSerializer(serializers.Serializer):

    title = serializers.CharField()

    total = serializers.IntegerField(
        required=False,
    )

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
    )

    data = serializers.JSONField(
        required=False,
    )