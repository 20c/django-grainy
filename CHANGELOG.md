
# Change Log

## [Unreleased]
### Added

- tests for django 2.1
- fix #33: easy namespace inheritance through related models

### Fixed

- admin inlines: sort by namespace alphabetically (#24)

### Changed

- move from facsimile to Ctl (#32)

### Deprecated
### Removed
### Security

## 1.6.2

### Fixed

- when applying perms to a grainy view response, make sure to return the proper container when it is empty

## 1.6.1

### Fixed

- Fixed issue with namespace formatting for grainy views that was introduced in 1.6.0 where trying to format using url parameters would raise a KeyError

## 1.6.0

### Added

- grainy view decorators can now access the request object when formatting namespaces
- you can now use extra keyword arguments passed to `Grainy.namespace` and `helpers.namespace` to further format the namespace string

### Changed

- grainy view decorators: renamed `explicit_object` to `explicit_instance`


## 1.5.0

### Added

- `util.Permissions.get` now accepts the `explicit` keyword argument
- `decorators.grainy_view` now accepts the `explicit_object` keyword argument

### Fixed

- `util.Permissions.get` now works correctly

### Changed

- `decorators.grainy_view` request GET parameters now available for namespace formatting
- `decorators.grainy_view` get_object() now available as `instance` for base namespace formatting if it exists
- `decorators.grainy_decorator` decorator namespaces can now be passed as lists in which case the resulting namespace is a joint namespace of all the elements


## 1.4.0

### Added

- implemented `decorators.grainy_view_response`
- implemented `decorators.grainy_json_view_response`
- implemented `decorators.grainy_rest_viewset_response`

### Changed

- `decorators.grainy_view` now simply decorates all response handlers
    with `decorators.grainy_view_response`
- `decorators.grainy_json_view` now simply decorates all response handlers
    with `decorators.grainy_json_view_response`
- `decorators.grainy_rest_viewset` now simply decorates all response handlers
    with `decorators.grainy_rest_viewset_response`

## 1.3.0

### Added

- grainy_model: allow specifying of custom instance namespace formatting
- grainy_view: impl explicit namespace handling during request gating

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
