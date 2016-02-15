# -*- coding: utf-8 -*-

from django.db import models
from django.db.utils import OperationalError
from django.utils.translation import ugettext_lazy as _


class SequenceMeta(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=127, unique=True)
    value = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _(u'SequenceMeta')
        verbose_name_plural = _(u'SequenceMetas')

    def increment(self, commit=True):
        self.value += 1
        if commit:
            self.save()

    def next_value(self, commit=True):
        self.value += 1
        if commit:
            self.save()
        return self.value

    @classmethod
    def create_if_not(cls, key):
        try:
            (seq, created) = SequenceMeta.objects.get_or_create(key=key)
            return seq
        except OperationalError:
            return None

    @classmethod
    def next(cls, key, commit=True):
        seq = SequenceMeta.create_if_not(key)
        return seq.next_value(commit)

    def __unicode__(self):
        return self.key + "__" + str(self.value)

