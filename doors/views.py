from django.shortcuts import render, get_object_or_404
from doors.models import *
from django.http import HttpResponse
from django.views.generic import DetailView

class SelfUserDetailView( DetailView ) :
    model               = User
    template_name       = 'doors/users/detail.html'
    context_object_name = 'user_object'

    def get_object( self ) :
        return self.request.user
