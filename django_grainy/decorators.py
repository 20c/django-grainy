from .models import GrainyHandler as _GrainyHandler

class grainy_model(object):

    def __init__(self, namespace=None):
        self.namespace = namespace

    def __call__(self, model):

        class Grainy(_GrainyHandler):
            pass

        Grainy.model = model

        if self.namespace is not None:
            namespace = self.namespace

            @classmethod
            def namespace_model(cls):
                return namespace.lower()
            Grainy.namespace_model = namespace_model

        model.Grainy = Grainy
        return model
