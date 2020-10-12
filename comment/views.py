from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.contenttypes.models import ContentType
from django.views import View
from blog.models import Post
from .forms import CommentForm


class AddCommentView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        bound_form = CommentForm(request.POST)
        if bound_form.is_valid():
            new_comment = bound_form.save()
            new_comment.author = request.user
            new_comment.content_type = ContentType.objects.get_for_model(Post)
            new_comment.object_id = post.id
            new_comment.save()
            return redirect(reverse('post_detail_url', args=[str(pk)]))
        else:
            context = {'post': post, 'comment_form': CommentForm,
                       'comments': post.comments.all()}
            return render(request, "blog/post_detail.html", context=context)
