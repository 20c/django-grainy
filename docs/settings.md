## GRAINY_ADMIN_REMOVE_DEFAULT_FORMS

If true the forms for vanilla django permissions will be removed from the admin UI

**default**: True

## GRAINY_ANONYMOUS_PERMS

Allows you to specify a set of permissions for AnonymousUser instances.

```py
GRAINY_ANONYMOUS_PERMS = {
  "a.b.c" : grainy.const.PERM_READ
}
```

**default**
```py
GRAINY_ANONYMOUS_PERMS = {}
```

## GRAINY_ANONYMOUS_GROUP

Can be set to a user group name. AnonymousUser permissions will be augmented
with permissions from that specified group.

**default**
```py
GRAINY_ANONYMOUS_GROUP = None
```

## GRAINY_DJANGO_OP_TO_FLAG

```dict``` used to convert a django admin operation to a grainy permission flag

**default**
```py
{!examples/settings/grainy_django_op_to_flag_predefined.py!}
```

## GRAINY_PERM_CHOICES

A list describing the possible permission flags

**default**
```py
{!examples/settings/grainy_perm_choices_crud.py!}
```

django-grainy comes with two predefined permission setups that you can use.

**predefined shortcuts**
```py
{!examples/settings/grainy_perm_choices_predefined.py!}
```

```py
{!examples/settings/grainy_perm_choices_predefined_rw.py!}
```


## GRAINY_REQUEST_METHOD_TO_FLAG

```dict``` used to convert a request method to a grainy permission flag

**default**:
```py
GRAINY_REQUEST_METHOD_TO_FLAG = getattr(settings, "GRAINY_REQUEST_METHOD_TO_FLAG", {
    "HEAD" : grainy.const.PERM_READ,
    "OPTIONS" : grainy.const.PERM_READ,
    "GET" : grainy.const.PERM_READ,
    "PUT" : grainy.const.PERM_UPDATE,
    "PATCH" : grainy.const.PERM_UPDATE,
    "POST" : grainy.const.PERM_CREATE,
    "DELETE" : grainy.const.PERM_DELETE,
})
```
