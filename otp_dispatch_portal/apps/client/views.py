import datetime
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, \
    DetailView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Import project components
from .models import Client, AuthorisedRepresentative
from .forms import ClientCreateForm, AuthRepCreateForm
from otp_dispatch_portal.apps.otp_dispatcher.forms import OneTimePasswordForm
from otp_dispatch_portal.apps.otp_dispatcher.views import otp_dispatcher_func
from otp_dispatch_portal.apps.otp_dispatcher.models import OneTimePasscode

# Create your views here.
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientCreateForm
    template_name = 'client/client_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return redirect('client_detail', pk=obj.pk)


class ClientDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Client
    template_name = 'client/client_detail.html'
    form_class = OneTimePasswordForm

    # Upon successful form submission return to client detail page.
    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk': self.object.id})

    # Pass key word arguments to the form view so it can limit auth_reps linked to this client.
    def get_form_kwargs(self):
        kwargs = super(ClientDetailView, self).get_form_kwargs()
        company = self.object
        # Add company to kwargs which will be used in OneTimePasswordForm queryset.
        kwargs['company'] = company
        return kwargs

    # Retrieve additional context data outside the Client model.
    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        # Pull AuthorisedRepresentative model data.
        context['auth_reps'] = AuthorisedRepresentative.objects.filter(company=self.kwargs['pk'])
        # Pull OneTimePasscode model data.
        context['otp_history'] = OneTimePasscode.objects.filter(company=self.kwargs['pk']).order_by('-created')
        # Pull OneTimePasswordForm and add to context data.
        context['form'] = self.get_form()
        context['now'] = datetime.datetime.now()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Don't save form data and add additional to instance.
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.company = self.object
        # Set what type of OTP is to be sent. Used by otp_dispatcher_func()
        if instance.destination == 'SMS':
            instance.dest_value = instance.auth_rep.mobile
        elif instance.destination == 'EML':
            instance.dest_value = instance.auth_rep.email
        instance.expire_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        # Send auth_rep and destination value to otp_dispatcher_func and receive 6 char OTP back.
        instance.otp_val = otp_dispatcher_func(auth_rep=instance.auth_rep, dest=instance.destination)
        # Save instance to DB.
        instance.save()
        return super(ClientDetailView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientCreateForm
    template_name = 'client/client_update.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.modified_by = self.request.user
        obj.save()
        return redirect('client_detail', pk=obj.pk)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        messages.info(self.request, 'Client deleted.')
        return reverse('dashboard')

class AuthRepCreateView(LoginRequiredMixin, CreateView):
    model = AuthorisedRepresentative
    form_class = AuthRepCreateForm
    template_name = 'client/auth_rep_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.company = get_object_or_404(Client, id=self.kwargs['client'])
        obj.created_by = self.request.user
        obj.save()
        return redirect('client_detail', pk=self.kwargs['client'])

class AuthRepUpdateView(LoginRequiredMixin, UpdateView):
    model = AuthorisedRepresentative
    form_class = AuthRepCreateForm
    template_name = 'client/auth_rep_update.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.modified_by = self.request.user
        obj.save()
        return redirect('client_detail', pk=self.kwargs['client'])

# Users are disabled never deleted. View not used.
# class AuthRepDeleteView(DeleteView):
#     model = AuthorisedRepresentative
#     template_name = 'confirm_delete.html'
#
#     def get_success_url(self):
#         messages.info(self.request, 'Authorised representative record deleted.')
#         return reverse('client_detail', kwargs={'pk': self.object.company.pk})