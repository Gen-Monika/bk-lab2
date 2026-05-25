# Game Host Manager

BlueKing Django SaaS course project for CMDB-based game host management.

## Features

- Business, set, and module cascading query through BlueKing CMDB.
- Host list query with filters for host name, operator, backup operator, and inner IP.
- Host detail panel.
- Local sample-data mode for development when CMDB access is unavailable.

## Routes

- `/hosts/`: host management page
- `/hosts/api/businesses/`: business list
- `/hosts/api/sets/?bk_biz_id=2`: set list
- `/hosts/api/modules/?bk_biz_id=2&bk_set_id=21`: module list
- `/hosts/api/hosts/?bk_biz_id=2`: host list
- `/hosts/api/hosts/<host_id>/`: host detail

## Local Development

Use the shared Python environment and set BlueKing environment variables as in the first lab.

For local UI testing without CMDB credentials or BlueKing login:

```powershell
$env:BKPAAS_ENVIRONMENT = "test"
python manage.py runserver 127.0.0.1:8003
```

Recommended checks:

```powershell
python manage.py check
$env:BKPAAS_ENVIRONMENT = "test"
python manage.py test hosts
```

## Course Material Note

The provided `CMDB - front-end code package.zip` is a Git LFS pointer file rather than a complete zip archive. This project implements the required UI with Django templates so the experiment can proceed without that damaged package.
