# L2 CMDB Host Manager Development Log

Date: 2026-05-25

## Summary

Started the second BlueKing SaaS course project for CMDB-based game host management. The provided front-end package is a Git LFS pointer instead of a complete zip, so the first implementation uses Django templates and the BlueKing component SDK directly.

## Changes

- Added the `hosts` Django app.
- Added `/hosts/` as the host management page.
- Added CMDB API endpoints for businesses, sets, modules, host lists, and host details.
- Added a Bootstrap-style page with cascading selectors, host filters, a host table, and a detail panel.
- Added automated tests for the core query flow.

## Maintenance Update

- Removed runtime fallback to local fabricated CMDB data so deployment failures and CMDB permission issues are shown as explicit API errors.
- Hid platform demo-only businesses such as `demo体验业务` from the business selector.
- Moved local host sample data out of business code and archived the retired file at `docs/archive/mock_data.py.bak`.
- Reworked tests to use internal mock CMDB responses, keeping fake hosts in the test layer only.
- Added front-end timeout and error-state handling so host search failures cannot leave the page stuck at `Searching hosts...`.
- Hid test-only CMDB sets, merged duplicate set/module names in selectors, and kept merged IDs searchable through `$in` conditions.
- Added suggested real CMDB host topology to README for course environment cleanup and host creation.
- Switched host list queries from `search_host` to the course-compatible `list_biz_hosts` API after the online ESB gateway reported `API not found` for `cc/search_host`.

## Verification

- `python manage.py check`: OK
- `BKPAAS_ENVIRONMENT=test python manage.py test hosts`: OK
