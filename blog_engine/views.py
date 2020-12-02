from django.shortcuts import redirect


def redirect_view(request):
    return redirect('posts_list_url', permanent=True)
