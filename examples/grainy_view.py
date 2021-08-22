from django.views import View as BaseView

from django_grainy.decorators import grainy_view


# grainy function view
@grainy_view(namespace="a.b.c")
def view(request):
    return HttpResponse()

# grainy class view
@grainy_view(namespace="a.b.c")
class View(BaseView):

    # will check for READ perms to "a.b.c", otherwise fails with 403
    def get(self, request):
        return HttpResonse()

    # will check for CREATE perms to "a.b.c", otherwise fails with 403
    def post(self, request):
        return HttpResponse()

    # will check for UPDATE perms to "a.b.c", otherwise fails with 403
    def put(self, request):
        return HttpResponse()

    # will check for UPDATE perms to "a.b.c", otherwise fails with 403
    def patch(self, request):
        return HttpResponse()

    # will check for DELETE perms to "a.b.c", otherwise fails with 403
    def delete(self, request):
        return HttpResponse()


# grainy view with formatted namespace
@grainy_view(namespace="detail.{id}")
def detail_view(request, id):
    return HttpResponse()

# you can also pass through flags for permissions checks
@grainy_view(
    namespace="detail.{id}",
    # require that the user has explicitly set permissions for the namespace
    explicit=True,
    # ignore the user's superuser priviledges
    ignore_grant_all=True
)
def detail_view(request, id):
    return HttpResponse()
