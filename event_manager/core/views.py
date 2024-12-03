from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"
    
    def get_context_data(self, **kwargs):
        """Context für das Template mit Daten anreichern."""
        ctx = super().get_context_data(**kwargs)
        ctx["hallo"] = "hallo hallo"
        return ctx
