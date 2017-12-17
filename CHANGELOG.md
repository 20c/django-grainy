
# Change Log

## [Unreleased]
### Added

- grainy_model: allow specifying of custom instance namespace formatting
- graint_view: impl explicit namespace handing during request gating

### Fixed
### Changed
### Deprecated
### Removed
### Security

## 1.2.1

### Fixed

- Template files not being installed

## 1.2.0

### Added

- Permissions.instances(): add `explicit` keyword argument
- Permissions.instances(): add `ignore_grant_all` keyword argument
- Permissions.check(): add `ignore_grant_all` keyword argument

## 1.1.0

### Added

- Passing a `tuple` or `list` to `helpers.namespace` will now return a joint namespace of all contained elements
- Implemented `util.Permissions.instances` method to retrieve all instances of a model according to permissions
- `decorators.grainy_view` decorator can now use url parameters to format it s namespace

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
