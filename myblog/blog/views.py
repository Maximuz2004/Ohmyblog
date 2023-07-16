from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{data["name"]} рекомендует тебе прочитать {post.title}'
            message = (f'Прочитай {post.title} по адресу: {post_url}\n\n '
                       f'{data["name"]} комментарии: {data["comments"]}')
            send_mail(subject, message, settings.EMAIL_ADMIN, [data['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
