# Managing user permissions

A user gets his permissions directly or from one of the auth Groups he is a member of

## Setting permissions

```py
{!examples/add_permissions.py!}
```
## Setting permissions in bulk

```py
{!examples/add_permissions_from_set.py!}
```

## Checking permissions

```py
{!examples/check_permissions.py!}
```

## Grainy Models

A django model can be initialized for grainy permissions using the
grainy_model decorator.

```py
{!examples/grainy_model.py!}
```

Afterwards the model can be used directly to set or check permissions to it

```py
{!examples/model_permissions.py!}
```

In the `grainy_model` decorator you can also specify if you want grainy to
treat the model as a child of another grainy model by using the `parent` parameter.

This also you to quickly chain namespaces with the child getting it's namespace
prefixed with the parent's namespace

```py
{!examples/grainy_model_parent.py!}
```

## Grainy views

A django view can be initialized for grainy permissions using the grainy_view
decorator.

When a view is made grainy it will automatically check for apropriate permissions to the specified namespace depending on the request method.

```py
{!examples/grainy_view.py!}
```

### Manually decorate view response handlers

The `grainy_view` decorator simply calls the apropriate response decorator on all the response handlers
in the view.

It follows that

```py
{!examples/grainy_view_manual_a.py!}
```

is the same as

```py
{!examples/grainy_view_manual_b.py!}
```

You may also use both decorators

```py
{!examples/grainy_view_manual_c.py!}
```

## Rest Framework Integration

Use the grainy_rest_viewset decorator to apply grainy permissions to the output of a django_rest_framework ViewSet. This means any content that the user does not have permission to view will be dropped from the api response.

```py
{!examples/grainy_rest_viewset.py!}
```

A user with `READ` permissions to `api.a` accessing this rest viewset would get this response

```py
[{"name":"Test model 1","id":1,"nested_dict":{"something":"public"}}]
```

While a user with `READ` permissions to `api.a` and `READ` permissions to `api.a.*.nested_dict.secret` would get this response

```py
[{"name":"Test model 1","id":1,"nested_dict":{"secret":{"hidden":"data"},"something":"public"}}]
```
