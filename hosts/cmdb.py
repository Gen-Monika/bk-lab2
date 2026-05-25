import logging

from django.conf import settings

from blueking.component.shortcuts import get_client_by_request

from . import mock_data

logger = logging.getLogger(__name__)


class CmdbService:
    def __init__(self, request):
        self.client = get_client_by_request(request)
        self.use_sample_data = getattr(settings, "CMDB_USE_SAMPLE_DATA", False)

    def list_businesses(self):
        params = {
            "fields": ["bk_biz_id", "bk_biz_name"],
            "page": {"start": 0, "limit": 200, "sort": ""},
        }
        return self._call(self.client.cc.search_business, params, mock_data.BUSINESSES)

    def list_sets(self, bk_biz_id):
        params = {
            "bk_biz_id": bk_biz_id,
            "fields": ["bk_set_id", "bk_set_name", "bk_biz_id"],
            "condition": {"bk_biz_id": bk_biz_id},
            "page": {"start": 0, "limit": 200, "sort": ""},
        }
        fallback = [row for row in mock_data.SETS if row["bk_biz_id"] == bk_biz_id]
        return self._call(self.client.cc.search_set, params, fallback)

    def list_modules(self, bk_biz_id, bk_set_id):
        params = {
            "bk_biz_id": bk_biz_id,
            "fields": ["bk_module_id", "bk_module_name", "bk_set_id", "bk_biz_id"],
            "condition": {"bk_biz_id": bk_biz_id, "bk_set_id": bk_set_id},
            "page": {"start": 0, "limit": 200, "sort": ""},
        }
        fallback = [
            row
            for row in mock_data.MODULES
            if row["bk_biz_id"] == bk_biz_id and row["bk_set_id"] == bk_set_id
        ]
        return self._call(self.client.cc.search_module, params, fallback)

    def list_hosts(self, filters):
        params = {
            "bk_biz_id": filters.get("bk_biz_id"),
            "page": {"start": 0, "limit": 200, "sort": "bk_host_id"},
        }
        if filters.get("bk_set_id") or filters.get("bk_module_id"):
            params["condition"] = []
        if filters.get("bk_set_id"):
            params["condition"].append(
                {"field": "bk_set_id", "operator": "$eq", "value": filters["bk_set_id"]}
            )
        if filters.get("bk_module_id"):
            params["condition"].append(
                {"field": "bk_module_id", "operator": "$eq", "value": filters["bk_module_id"]}
            )
        host_filter = self._host_property_filter(filters)
        if host_filter["rules"]:
            params["host_property_filter"] = host_filter
        return self._call(self.client.cc.search_host, params, self._filter_mock_hosts(filters))

    def get_host_detail(self, host_id):
        params = {
            "bk_host_id": host_id,
            "fields": [
                "bk_host_id",
                "bk_host_innerip",
                "bk_host_name",
                "bk_os_name",
                "bk_cpu",
                "bk_mem",
                "operator",
                "bk_bak_operator",
            ],
        }
        fallback = [row for row in mock_data.HOSTS if row["bk_host_id"] == host_id]
        rows = self._call(self.client.cc.get_host_base_info, params, fallback)
        return rows[0] if rows else None

    def _call(self, api, params, fallback):
        if self.use_sample_data:
            return fallback
        try:
            result = api(params)
        except Exception as err:
            logger.warning("CMDB API call failed, using local sample data: %s", err)
            return fallback
        if not result.get("result"):
            logger.warning("CMDB API returned error, using local sample data: %s", result.get("message"))
            return fallback
        data = result.get("data") or {}
        rows = data.get("info") if isinstance(data, dict) else data
        return rows or fallback

    def _host_property_filter(self, filters):
        host_filter = {"condition": "AND", "rules": []}
        for field in ("bk_host_name", "operator", "bk_bak_operator", "bk_host_innerip"):
            value = filters.get(field)
            if value:
                host_filter["rules"].append(
                    {"field": field, "operator": "contains", "value": value}
                )
        return host_filter

    def _filter_mock_hosts(self, filters):
        rows = mock_data.HOSTS
        for key in ("bk_biz_id", "bk_set_id", "bk_module_id"):
            value = filters.get(key)
            if value:
                rows = [row for row in rows if row.get(key) == value]
        for key in ("bk_host_name", "operator", "bk_bak_operator", "bk_host_innerip"):
            value = filters.get(key)
            if value:
                rows = [row for row in rows if value.lower() in str(row.get(key, "")).lower()]
        return rows
