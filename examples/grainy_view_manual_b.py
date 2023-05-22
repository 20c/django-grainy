from django.views import BaseView

from django_grainy.decorators import grainy_view_response


# grainy class view
class View(BaseView):
    # will check for READ perms to "a.b.c", otherwise fails with 403
    @grainy_view_response(namespace="a.b.c")
    def get(self, request):
        return HttpResonse()

    # will check for CREATE perms to "a.b.c", otherwise fails with 403
    @grainy_view_response(namespace="a.b.c")
    def post(self, request):
        return HttpResponse()

    # will check for UPDATE perms to "a.b.c", otherwise fails with 403
    @grainy_view_response(namespace="a.b.c")
    def put(self, request):
        return HttpResponse()

    # will check for UPDATE perms to "a.b.c", otherwise fails with 403
    @grainy_view_response(namespace="a.b.c")
    def patch(self, request):
        return HttpResponse()

    # will check for DELETE perms to "a.b.c", otherwise fails with 403
    @grainy_view_response(namespace="a.b.c")
    def delete(self, request):
        return HttpResponse()
