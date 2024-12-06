from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect


def pilars(request):
    context = {

    }
    return render(request, 'auth/pillars.html', context)