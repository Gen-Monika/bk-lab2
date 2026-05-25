from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from hosts import views

TEST_BUSINESSES = [
    {"bk_biz_id": 1, "bk_biz_name": "demo\u4f53\u9a8c\u4e1a\u52a1"},
    {"bk_biz_id": 2, "bk_biz_name": "Arena Ops"},
]

TEST_SETS = [
    {"bk_biz_id": 2, "bk_set_id": 21, "bk_set_name": "South China Zone"},
    {"bk_biz_id": 2, "bk_set_id": 22, "bk_set_name": "East China Zone"},
]

TEST_MODULES = [
    {"bk_biz_id": 2, "bk_set_id": 21, "bk_module_id": 211, "bk_module_name": "Login Service"},
    {"bk_biz_id": 2, "bk_set_id": 21, "bk_module_id": 212, "bk_module_name": "Battle Service"},
    {"bk_biz_id": 2, "bk_set_id": 22, "bk_module_id": 221, "bk_module_name": "Gateway Service"},
]

TEST_HOSTS = [
    {
        "bk_host_id": 1001,
        "bk_biz_id": 2,
        "bk_set_id": 21,
        "bk_module_id": 211,
        "bk_host_innerip": "10.0.1.11",
        "bk_host_name": "login-01",
        "bk_os_name": "CentOS",
        "bk_cpu": 8,
        "bk_mem": 16384,
        "operator": "alice",
        "bk_bak_operator": "bob",
        "cloud_area": "default area",
    },
    {
        "bk_host_id": 1002,
        "bk_biz_id": 2,
        "bk_set_id": 21,
        "bk_module_id": 212,
        "bk_host_innerip": "10.0.1.21",
        "bk_host_name": "battle-01",
        "bk_os_name": "Ubuntu",
        "bk_cpu": 16,
        "bk_mem": 32768,
        "operator": "carol",
        "bk_bak_operator": "alice",
        "cloud_area": "default area",
    },
    {
        "bk_host_id": 1003,
        "bk_biz_id": 2,
        "bk_set_id": 22,
        "bk_module_id": 221,
        "bk_host_innerip": "10.0.2.31",
        "bk_host_name": "gateway-01",
        "bk_os_name": "TencentOS",
        "bk_cpu": 8,
        "bk_mem": 16384,
        "operator": "dave",
        "bk_bak_operator": "erin",
        "cloud_area": "default area",
    },
]


class FakeCmdbApi:
    def __init__(self):
        self.fail_next_search_business = False

    def search_business(self, params):
        if self.fail_next_search_business:
            return {"result": False, "message": "CMDB unavailable", "data": None}
        return {"result": True, "data": {"info": TEST_BUSINESSES}}

    def search_set(self, params):
        bk_biz_id = params["bk_biz_id"]
        rows = [row for row in TEST_SETS if row["bk_biz_id"] == bk_biz_id]
        return {"result": True, "data": {"info": rows}}

    def search_module(self, params):
        condition = params["condition"]
        rows = [
            row
            for row in TEST_MODULES
            if row["bk_biz_id"] == condition["bk_biz_id"] and row["bk_set_id"] == condition["bk_set_id"]
        ]
        return {"result": True, "data": {"info": rows}}

    def search_host(self, params):
        rows = TEST_HOSTS
        bk_biz_id = params.get("bk_biz_id")
        if bk_biz_id:
            rows = [row for row in rows if row["bk_biz_id"] == bk_biz_id]
        for condition in params.get("condition", []):
            rows = [row for row in rows if row.get(condition["field"]) == condition["value"]]
        for rule in params.get("host_property_filter", {}).get("rules", []):
            value = str(rule["value"]).lower()
            rows = [row for row in rows if value in str(row.get(rule["field"], "")).lower()]
        return {"result": True, "data": {"info": rows}}

    def get_host_base_info(self, params):
        rows = [row for row in TEST_HOSTS if row["bk_host_id"] == params["bk_host_id"]]
        return {"result": True, "data": {"info": rows}}


class FakeBlueKingClient:
    def __init__(self):
        self.cc = FakeCmdbApi()


class HostManagerTests(TestCase):
    def setUp(self):
        for view in (
            views.index,
            views.businesses,
            views.sets,
            views.modules,
            views.hosts,
            views.host_detail,
        ):
            view.login_exempt = True
        self.client = Client()
        self.fake_client = FakeBlueKingClient()
        self.client_patch = patch("hosts.cmdb.get_client_by_request", return_value=self.fake_client)
        self.client_patch.start()

    def tearDown(self):
        self.client_patch.stop()

    def test_index_page_renders(self):
        response = self.client.get(reverse("hosts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Game Host Manager")

    def test_business_set_module_chain(self):
        response = self.client.get(reverse("hosts:businesses"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["result"])
        business_names = [item["bk_biz_name"] for item in response.json()["data"]]
        self.assertNotIn("demo\u4f53\u9a8c\u4e1a\u52a1", business_names)

        response = self.client.get(reverse("hosts:sets"), {"bk_biz_id": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"][0]["bk_set_id"], 21)

        response = self.client.get(reverse("hosts:modules"), {"bk_biz_id": 2, "bk_set_id": 21})
        self.assertEqual(response.status_code, 200)
        module_names = [item["bk_module_name"] for item in response.json()["data"]]
        self.assertIn("Login Service", module_names)

    def test_host_list_and_detail(self):
        response = self.client.get(reverse("hosts:hosts"), {"bk_biz_id": 2, "bk_set_id": 21})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 2)

        response = self.client.get(reverse("hosts:host_detail", args=[1001]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["bk_host_innerip"], "10.0.1.11")

    def test_host_filters_are_applied(self):
        response = self.client.get(
            reverse("hosts:hosts"),
            {"bk_biz_id": 2, "bk_host_name": "gateway"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"][0]["bk_host_name"], "gateway-01")

    def test_cmdb_error_is_reported(self):
        self.fake_client.cc.fail_next_search_business = True

        response = self.client.get(reverse("hosts:businesses"))

        self.assertEqual(response.status_code, 502)
        self.assertFalse(response.json()["result"])
        self.assertEqual(response.json()["message"], "CMDB unavailable")
