from rest_framework import serializers as sz

__all__ = ["BranchSerializer", "TraderSerializer", "ClusterManagerSerializer"]


class BranchSerializer(sz.Serializer):
    branch_code = sz.IntegerField()
    branch_name = sz.CharField(max_length=255)
    address = sz.CharField(allow_null=True, required=False)


class TraderSerializer(sz.Serializer):
    branch_code = sz.IntegerField()
    branch_name = sz.CharField(max_length=255)
    trader_id = sz.CharField(max_length=255)
    trader_name = sz.CharField(max_length=255)


class ClusterManagerSerializer(sz.Serializer):
    branch_code = sz.IntegerField()
    branch_name = sz.CharField(max_length=255)
    region_id = sz.CharField(max_length=255)
    region_name = sz.CharField(max_length=255)
    manager_name = sz.CharField(max_length=255)
