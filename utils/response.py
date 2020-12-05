# -*- coding: utf-8 -*-

from django.http import JsonResponse


def __response_data(status_code=200, message=None, data={}, **kwargs):
    # return dict({
    #     'status': status_code,
    #     'message': message,
        #  'data': data,
    #  }, **kwargs)
    # data.update({
    #     'status': status_code,
    #     'message': message,
    # })
    return data
    


def json_response(status_code=200, message=None, data={}, **kwargs):
    return JsonResponse(__response_data(status_code, message,data,**kwargs), safe=False)
