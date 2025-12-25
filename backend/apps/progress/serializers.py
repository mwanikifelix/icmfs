from rest_framework import serializers
from .models import DailyProgress
from .models import EVMSnapshot


class DailyProgressSerializer(serializers.ModelSerializer):
    planned_value = serializers.SerializerMethodField()
    earned_value = serializers.SerializerMethodField()
    cpi = serializers.SerializerMethodField()
    spi = serializers.SerializerMethodField()

    class Meta:
        model = DailyProgress
        fields = [
            "id",
            "project",
            "report_date",
            "work_done_description",
            "planned_percentage",
            "actual_percentage",
            "actual_cost",
            "approved",
            "planned_value",
            "earned_value",
            "cpi",
            "spi",
            "created_at",
        ]

    def get_planned_value(self, obj):
        return obj.planned_value()

    def get_earned_value(self, obj):
        return obj.earned_value()

    def get_cpi(self, obj):
        return obj.cost_performance_index()

    def get_spi(self, obj):
        return obj.schedule_performance_index()


class DailyProgressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProgress
        fields = [
            "project",
            "report_date",
            "work_done_description",
            "planned_percentage",
            "actual_percentage",
            "actual_cost",
        ]



class EVMSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVMSnapshot
        fields = "__all__"
