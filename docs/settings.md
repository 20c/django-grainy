## GRAINY_ADMIN_REMOVE_DEFAULT_FORMS

If true the forms for vanilla django permissions will be removed from the admin UI

**default**: True

## GRAINY_DJANGO_OP_TO_FLAG

```dict``` used to convert a django admin operation to a grainy permission flag

**default**
```py
{!examples/settings/grainy_django_op_to_flag_predefined.py!}
```

## GRAINY_PERM_CHOICES

A list describing the possible permission flags

```py
{!examples/settings/grainy_perm_choices_crud.py!}
```

django-grainy comes with two predefined permission setups that you can use.

**default**
```py
{!examples/settings/grainy_perm_choices_predefined.py!}
```
