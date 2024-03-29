from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post

# posts = [
#     {
#         'author': 'Rajat Singh',
#         'title': 'Blog Post 1',
#         'content': 'My First Blog',
        
#         'date_posted': '19 August 2023'
#     },
#     {
#         'author': 'Rahul Singh',
#         'title': 'Blog Post 2',
#         'content': 'My Second Blog',
#         'date_posted': '20 August 2023'
#     }
# ]

def home(request):
    # to get list of all Post model
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_list.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_list.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        users = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=users).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()

        if post.author == self.request.user:
            return True
        
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if post.author == self.request.user:
            return True
        
        return False




def about(request):
    return render(request, 'blog/about.html', {'task': 'About'})
    #return HttpResponse('<h1>Blog About</h1>')
