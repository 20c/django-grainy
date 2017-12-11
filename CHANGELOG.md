
# Change Log

## [Unreleased]
### Added
- Passing a `tuple` or `list` to `helpers.namespace` will now return a joint namespace of all contained elements
### Fixed
### Changed
### Deprecated
### Removed
### Security

## 1.0.0

### Added

- grainy authentication backend
- django admin integration
- str_flags function
- PermissioManager.add_permission
- Default permissions for AnonymousUser
- decorators.grainy_view
- decorators.grainy_rest_viewset
- helpers.dict_get_namespace
- helpers.request_method_to_flag
- helpers.request_to_flag
- util.Permissions.grant_all property
- conf.REQUEST_METHOD_TO_FLAG

### Fixed

- util.Permissions now accepts AnonynmousUser as object

### Changed

- renamed `convert_flags` to `int_flags`
- moved `str_flags` and `int_flags` functions from util.py to helpers.py
- moved `namespace` function from util.py to models.py
- removed `clear` argument from `PermissionManager.add_permission_set`
