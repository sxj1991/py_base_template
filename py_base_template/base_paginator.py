from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.request import Request


# 自定义分页器
class PageMixin(object):

    @staticmethod
    def build_base_paginator(request: Request, data: list, serializer=None):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(data, limit)
        try:
            paged = paginator.page(page)
        except PageNotAnInteger:
            paged = paginator.page(1)
        except EmptyPage:
            paged = paginator.page(paginator.num_pages)
        return {
            'objects': serializer(instance=paged, many=True).data if serializer else paged.object_list,
            'paging': {
                'limit': int(limit),
                'page': int(page),
                'total': int(paginator.count),
            }
        }
