
# Change Log

## [Unreleased]
### Added
- grainy authentication backend
- django admin integration
- str_flags function
- PermissioManager.add_permission
- decorators.grainy_rest_viewset
- helpers.dict_get_namespace
- util.Permissions.grant_all property
### Fixed
- util.Permissions now accepts AnonynmousUser as object
### Changed
- renamed `convert_flags` to `int_flags`
- moved `str_flags` and `int_flags` functions from util.py to helpers.py
- moved `namespace` function from util.py to models.py
- removed `clear` argument from `PermissionManager.add_permission_set`
### Deprecated
### Removed
### Security
