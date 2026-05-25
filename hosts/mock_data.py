BUSINESSES = [
    {"bk_biz_id": 2, "bk_biz_name": "Arena Ops"},
    {"bk_biz_id": 3, "bk_biz_name": "Frontier Test"},
]

SETS = [
    {"bk_biz_id": 2, "bk_set_id": 21, "bk_set_name": "South China Zone"},
    {"bk_biz_id": 2, "bk_set_id": 22, "bk_set_name": "East China Zone"},
    {"bk_biz_id": 3, "bk_set_id": 31, "bk_set_name": "Staging Zone"},
]

MODULES = [
    {"bk_biz_id": 2, "bk_set_id": 21, "bk_module_id": 211, "bk_module_name": "Login Service"},
    {"bk_biz_id": 2, "bk_set_id": 21, "bk_module_id": 212, "bk_module_name": "Battle Service"},
    {"bk_biz_id": 2, "bk_set_id": 22, "bk_module_id": 221, "bk_module_name": "Gateway Service"},
    {"bk_biz_id": 3, "bk_set_id": 31, "bk_module_id": 311, "bk_module_name": "Test Service"},
]

HOSTS = [
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
    {
        "bk_host_id": 1004,
        "bk_biz_id": 3,
        "bk_set_id": 31,
        "bk_module_id": 311,
        "bk_host_innerip": "10.0.3.41",
        "bk_host_name": "test-01",
        "bk_os_name": "CentOS",
        "bk_cpu": 4,
        "bk_mem": 8192,
        "operator": "frank",
        "bk_bak_operator": "grace",
        "cloud_area": "default area",
    },
]
