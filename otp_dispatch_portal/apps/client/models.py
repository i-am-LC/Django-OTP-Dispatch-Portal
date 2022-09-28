from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_created_by')
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=True, blank=True, related_name='client_modified_by')
    company_name = models.CharField(max_length=254)

    def __str__(self):
        return self.company_name


class AuthorisedRepresentative(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_rep_created_by')
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    null=True, blank=True, related_name='auth_rep_modified_by')
    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='auth_rep_company')
    email = models.EmailField()
    mobile = models.CharField(max_length=12)
    firstname = models.CharField(max_length=254)
    surname = models.CharField(max_length=254)
    role = models.CharField(max_length=254)
    country = models.CharField(max_length=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.firstname) + ' ' + str(self.surname)
