from django_grainy.remote import Authenticator, ProvideGet, ProvideLoad


class GrainyRequestAuthenticator(Authenticator):
    def authenticate(self, request):
        # pseudo-code for handling a token authentication
        handle_token_authentication(request)

urlpatterns += [
    # grainy
    path("grainy/get/<str:namespace>/", ProvideGet.as_view(authenticator_cls=GrainyRequestAuthenticator), name="grainy-get"),
    path("grainy/load/", ProvideLoad.as_view(authenticator_cls=GrainyRequestAuthenticator), name="grainy-load"),
]
