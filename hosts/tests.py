from django.test import Client, TestCase, override_settings
from django.urls import reverse

from hosts import views


@override_settings(CMDB_USE_SAMPLE_DATA=True)
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

    def test_index_page_renders(self):
        response = self.client.get(reverse("hosts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Game Host Manager")

    def test_business_set_module_chain(self):
        response = self.client.get(reverse("hosts:businesses"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["result"])

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
