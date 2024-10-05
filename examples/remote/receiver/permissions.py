import django_grainy.remote


class RemotePermissions(django_grainy.remote.Permissions):
    def __init__(self, obj):
        super().__init__(
            obj,
            url_load="http://localhost:8000/grainy/load",
            url_get="http://localhost:8000/grainy/get",
        )

    def prepare_request(self, params, headers):
        try:
            key = self.obj.key_set.first().key
            headers.update(Authorization=f"token {key}")
        except AttributeError:
            pass
