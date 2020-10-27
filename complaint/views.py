from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .utils import ObjectComplaintFunc

@login_required
def PostComplaintView(request, pk):
    print('lala')
    return redirect(reverse('post_detail_url', args=[str(pk)]))

@login_required
def CommentComplaintView(request, pk):
    pass
