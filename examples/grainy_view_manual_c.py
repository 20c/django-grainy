from django.views import BaseView

from django_grainy.decorators import grainy_view, grainy_view_response


# grainy class view
@grainy_view(namespace="a.b.c")
class View(BaseView):

    # will check for READ perms to "a.b.c", otherwise fails with 403
    def get(self, request):
        return HttpResonse()

    # will check for CREATE perms to "x.y.z", otherwise fails with 403
    @grainy_view_response(namespace="x.y.z")
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
