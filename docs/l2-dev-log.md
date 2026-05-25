# L2 CMDB Host Manager Development Log

Date: 2026-05-25

## Summary

Started the second BlueKing SaaS course project for CMDB-based game host management. The provided front-end package is a Git LFS pointer instead of a complete zip, so the first implementation uses Django templates and the BlueKing component SDK directly.

## Changes

- Added the `hosts` Django app.
- Added `/hosts/` as the host management page.
- Added CMDB API endpoints for businesses, sets, modules, host lists, and host details.
- Added a local sample-data mode through `CMDB_USE_SAMPLE_DATA`.
- Added a Bootstrap-style page with cascading selectors, host filters, a host table, and a detail panel.
- Added automated tests for the core query flow.

## Verification

- `python manage.py check`: OK
- `BKPAAS_ENVIRONMENT=test python manage.py test hosts`: OK
