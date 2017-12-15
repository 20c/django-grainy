from django_grainy.decorators import grainy_view
from django.views import View as BaseView

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
