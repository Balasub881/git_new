from django.http import request
from django.utils.datastructures import MultiValueDictKeyError

try:
    is_private = request.POST['is_private']
except MultiValueDictKeyError:
    is_private = False