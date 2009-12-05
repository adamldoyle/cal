from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from mixins.models import UserMixin, DateMixin
import datetime

class ScheduledEvent(UserMixin, DateMixin):
    date = models.DateField('date scheduled')
    type = models.CharField(max_length=30)
    
    def base_class(self):
        return getattr(self, self.type)
    
    def __unicode__(self):
        return self.base_class().__unicode__()
    
    def get_absolute_url(self):
        return self.base_class().get_absolute_url()
    
    def deleteUrl(self):
        return self.base_class().deleteUrl()
    
    def save(self):
        self.type = self.__class__.__name__.lower()
        super(ScheduledEvent, self).save()