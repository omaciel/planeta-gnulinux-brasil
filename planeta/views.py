# Create your views here.
# Create your views here.
from django.shortcuts import render_to_response

from models import Post

def post(request, post_id):
    post = Post.objects.get(id=artigo_id)
        return render_to_response('planeta/post.html', locals())
