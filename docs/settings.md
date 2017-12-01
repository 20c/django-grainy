## GRAINY_ADMIN_REMOVE_DEFAULT_FORMS
**default**: True

If true the forms for vanilla django permissions will be removed from the admin UI

## GRAINY_PERM_CHOICES

A list describing the possible permission flags

```py
{!examples/settings/grainy_perm_choices_crud.py!}
```

django-grainy comes with two predefined permission setups that you can use. It will default to ```PERM_CHOICES_CRUD```.

```py
{!examples/settings/grainy_perm_choices_predefined.py!}
```
