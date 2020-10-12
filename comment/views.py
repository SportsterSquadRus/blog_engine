from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.contenttypes.models import ContentType
from django.views import View
from blog.models import Post
from .forms import CommentForm
from time import time


class AddCommentView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        bound_form = CommentForm(request.POST)
        if bound_form.is_valid() and ('last_comment' not in request.session or (time() - request.session['last_comment']) > 5):
            new_comment = bound_form.save()
            new_comment.author = request.user
            new_comment.content_type = ContentType.objects.get_for_model(Post)
            new_comment.object_id = post.id
            new_comment.save()
            request.session['last_comment'] = time()
            return redirect(reverse('post_detail_url', args=[str(pk)]))
        else:
            return redirect(reverse('post_detail_url', args=[str(pk)]))
