from django.http import JsonResponse
from django.shortcuts import render

from .cmdb import CmdbService


def index(request):
    return render(request, "hosts/index.html")


def businesses(request):
    return _ok(CmdbService(request).list_businesses())


def sets(request):
    bk_biz_id = _int_query(request, "bk_biz_id")
    if not bk_biz_id:
        return _bad_request("bk_biz_id is required")
    return _ok(CmdbService(request).list_sets(bk_biz_id))


def modules(request):
    bk_biz_id = _int_query(request, "bk_biz_id")
    bk_set_id = _int_query(request, "bk_set_id")
    if not bk_biz_id or not bk_set_id:
        return _bad_request("bk_biz_id and bk_set_id are required")
    return _ok(CmdbService(request).list_modules(bk_biz_id, bk_set_id))


def hosts(request):
    filters = {
        "bk_biz_id": _int_query(request, "bk_biz_id"),
        "bk_set_id": _int_query(request, "bk_set_id"),
        "bk_module_id": _int_query(request, "bk_module_id"),
        "bk_host_name": request.GET.get("bk_host_name", "").strip(),
        "operator": request.GET.get("operator", "").strip(),
        "bk_bak_operator": request.GET.get("bk_bak_operator", "").strip(),
        "bk_host_innerip": request.GET.get("bk_host_innerip", "").strip(),
    }
    if not filters["bk_biz_id"]:
        return _bad_request("bk_biz_id is required")
    return _ok(CmdbService(request).list_hosts(filters))


def host_detail(request, host_id):
    data = CmdbService(request).get_host_detail(host_id)
    if data is None:
        return JsonResponse({"result": False, "message": "host not found", "data": None}, status=404)
    return _ok(data)


def _ok(data):
    return JsonResponse({"result": True, "message": "success", "data": data})


def _bad_request(message):
    return JsonResponse({"result": False, "message": message, "data": None}, status=400)


def _int_query(request, key):
    value = request.GET.get(key)
    if value in (None, ""):
        return None
    try:
        return int(value)
    except ValueError:
        return None
