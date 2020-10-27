from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .utils import ObjectComplaintFunc
from blog.models import Post

@login_required
def PostComplaintView(request, pk):
    ObjectComplaintFunc(request, pk, Post)
    return redirect(reverse('post_detail_url', args=[str(pk)]))

@login_required
def CommentComplaintView(request, pk):
    pass
