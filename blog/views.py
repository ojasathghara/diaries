from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin # Allows only those post to be edited which are created by user
)
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
import diaries.settings as diaries_settings

# Create your views here.
def home(request):
    # not using this
    posts = Post.objects.all();
    context = {
        'posts': posts,
        'title': 'Home'
    }

    return render(request, 'blog/home.html', context=context)

# class based views by default looks for template as: <appname>/<model>_<viewtype>.html ex: blog/post_list.html
class PostListView(ListView):

    model = Post    # get model you want to display as list
    template_name = 'blog/home.html' 
    paginate_by = 7    # no of posts in one page (see corey schafer pagination youtube)
    context_object_name = 'posts'   # the context dict is as it is. This line adds a new key value pair to context dict as {'posts': get_queryset(self)}.

    def get_queryset(self):     # returns the query wanted by the ListView
        return Post.objects.all().order_by('-date_posted')   

    def get_context_data(self, **kwargs):

        context = super(PostListView, self).get_context_data(**kwargs)
        context['title'] = 'Home'
        
        if diaries_settings.DEBUG == True:
            import os
            context['pid'] = os.getpid()

        return context


class PostDetailView(DetailView):

    model = Post    # automatically takes only one object based on url
    # using default view: blog/post_detail.html
    # using default name for context variable (object)

class PostCreateView(LoginRequiredMixin, CreateView):
# if not logged in, redirect to login url (defined in project settings)

    model = Post
    # using default view: blog/post_form.html
    # using default name for context variable (form)
    fields = ['title', 'content']

    # override the form valid method to get current user while creating a new post
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        return super().form_valid(form);
        # after successfully creating a post it redirects to the post url
        # the post url is fetched by the get_absolute_url method defined in the model Post

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# more or less same as create, uses the same template too!

    model = Post
    fields = ['title', 'content']

    # LoginRequired overriding the default method to custom check for form validity
    def form_valid(self, form):
        form.instance.author = self.request.user    # instance means current instance of the form (the specific post in this case)
        
        return super().form_valid(form);
    
    # LoginReqredMixin overriding the default method to custom check for user validity of the post
    def test_func(self):

        """
            get_object() looks for a pk_url_kwarg argument in the arguments to the view; if this argument is found, this method performs a primary-key based lookup using that value. If this argument is not found, it looks for a slug_url_kwarg argument, and performs a slug lookup using the slug_field.

            Changed in Django 1.8:
                When query_pk_and_slug is True, get_object() will perform its lookup using both the primary key and the slug.

            gets the post object of this requested post form model = Post
            Provides a mechanism for looking up an object associated with the current HTTP request.
        """
        post = self.get_object()    
    
        if self.request.user == post.author:
            return True
        else:
            return False

        return super().test_func()

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    #default template is blog/post_confirm_delete.html
    
    success_url = '/blog/'   # important! redirects to this url after deletion

    # LoginReqredMixin
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        else:
            return False

        return super().test_func()

def about(request):
    context = {
        'title': 'About'
    }

    return render(request, 'blog/about.html', context=context)

class UserPostList(ListView):
    # cannot paginate in Detail view, pagination only allowed in detailed view.
    # see https://stackoverflow.com/questions/25569551/pagination-from-a-django-detailview

    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        username = self.kwargs['username']  # get username from url
        user = get_object_or_404(User, username=username)

        return Post.objects.filter(author=user).order_by('-date_posted')


    def get_context_data(self, **kwargs):  
        username = self.kwargs['username'] # this kwarg is different dictionary than the argument one. This kwargs dict contains args passed to url       
        user_obj = get_object_or_404(User, username=username) # get the user object passed to url

        context = super(UserPostList, self).get_context_data(**kwargs) # fetch the context dictionary

        context['author'] = user_obj
        context['title'] = 'Profile'

        return context
