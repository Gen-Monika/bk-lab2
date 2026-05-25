# Game Host Manager

BlueKing Django SaaS course project for CMDB-based game host management.

## Features

- Business, set, and module cascading query through BlueKing CMDB.
- Host list query with filters for host name, operator, backup operator, and inner IP.
- Host detail panel.
- Clear CMDB error reporting without showing fabricated host records.
- Duplicate set/module names are merged in the selector, and test-only sets are hidden from the course workflow.

## Routes

- `/hosts/`: host management page
- `/hosts/api/businesses/`: business list
- `/hosts/api/sets/?bk_biz_id=2`: set list
- `/hosts/api/modules/?bk_biz_id=2&bk_set_id=21`: module list
- `/hosts/api/hosts/?bk_biz_id=2`: host list
- `/hosts/api/hosts/<host_id>/`: host detail

## Local Development

Use the shared Python environment and set BlueKing environment variables as in the first lab.

For local UI testing without BlueKing login:

```powershell
$env:BKPAAS_ENVIRONMENT = "test"
python manage.py runserver 127.0.0.1:8003
```

The running application reads data from BlueKing CMDB. If CMDB is unavailable, the page reports the API error instead of showing fabricated host records. Requests time out after 15 seconds so the UI does not stay in a loading state. Automated tests use internal mock CMDB responses.

Host list queries use the course-compatible `client.cc.list_biz_hosts` API. Some BlueKing community environments do not publish `client.cc.search_host` through the ESB gateway, which would raise `API not found`.

Recommended checks:

```powershell
python manage.py check
$env:BKPAAS_ENVIRONMENT = "test"
python manage.py test hosts
```

## Course Material Note

The provided `CMDB - front-end code package.zip` is a Git LFS pointer file rather than a complete zip archive. This project implements the required UI with Django templates so the experiment can proceed without that damaged package.

Demo-only businesses returned by the platform, such as `demo体验业务`, are hidden from the business selector to keep the course workflow focused on real experiment data. The retired local sample data file is archived at `docs/archive/mock_data.py.bak` for maintenance traceability and is not imported by runtime code.

## Suggested CMDB Records

For the course demonstration, keep one real business and add a small, non-duplicated host topology in BlueKing CMDB:

- Business: `小游戏教学演示`
- Sets: `登录区`, `战斗区`, `网关区`
- Modules: `Login Service`, `Battle Service`, `Gateway Service`
- Hosts: at least three records with distinct inner IPs, host names, operators, and backup operators.
