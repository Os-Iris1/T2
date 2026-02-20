from django.core.paginator import Paginator
from classifier.data.model import ChurnData

class ChurnDataRepository:
    
    @staticmethod
    def get_first_n_records(n=15):
        return ChurnData.objects.all()[:n]
    
    @staticmethod
    def get_records_with_offset(limit=15, offset=0):
        return ChurnData.objects.all()[offset:offset + limit]
    
    @staticmethod
    def get_paginated_records(page=1, per_page=15):
        paginator = Paginator(ChurnData.objects.all(), per_page)
        return paginator.get_page(page)
    
    @staticmethod
    def get_total_count():
        return ChurnData.objects.count()
    
    @staticmethod
    def get_records_by_ids(id_list):
        return ChurnData.objects.filter(id__in=id_list)
    
    @staticmethod
    def get_records_filtered(**filters):
        return ChurnData.objects.filter(**filters)