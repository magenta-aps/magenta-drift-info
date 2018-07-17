from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Q
from django.views import generic

from .models import Event, Customer, System, Server


class IndexView(generic.ListView):
    context_object_name = 'customers'
    template_name = 'magentadriftinfo/index.html'
    queryset = Customer.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['systems'] = System.objects.all()
        context['servers'] = Server.objects.all()
        print(context['systems'])
        for system in context['systems']:
            print(system.customers.all())
        return context


class CustomerIndexView(generic.ListView):
    model = Customer
    template_name = 'magentadriftinfo/customer_index.html'
    context_object_name = 'customers'


class SystemIndexView(generic.ListView):
    model = System
    template_name = 'magentadriftinfo/system_index.html'
    context_object_name = 'systems'


class ServerIndexView(generic.ListView):
    model = Server
    template_name = 'magentadriftinfo/server_index.html'
    context_object_name = 'servers'


class DetailView(TemplateResponseMixin, View):
    template_name = 'magentadriftinfo/detail.html'
    model = Event
    ordering = '-startTime'

    def get_context_data(self, **kwargs):
        qs = Event.objects.all()
        filter = {}
        if 'server' in self.kwargs:
            qs = qs.filter(servers__name=self.kwargs['server'])
        if 'system' in self.kwargs:
            qs = qs.filter(systems__name=self.kwargs['system'])
        if 'customer' in self.kwargs:
            qs = qs.filter(
                Q(servers__customers__name=self.kwargs['customer']) |
                Q(systems__customers__name=self.kwargs['customer'])
            )
        qs = qs.distinct().order_by(self.ordering)

        context = {
            'active_qs': Event.filter_active(qs),
            'former_qs': Event.filter_former(qs),
            'future_qs': Event.filter_future(qs),
        }
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
