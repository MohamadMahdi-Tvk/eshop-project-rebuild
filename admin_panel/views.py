from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from article_module.models import Article
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@permission_required('site_module.view_adminpanel', raise_exception=True)
def index(request: HttpRequest):
    return render(request, 'admin_panel/home/index.html')


class ArticlesListView(PermissionRequiredMixin, ListView):
    model = Article
    paginate_by = 12
    template_name = 'admin_panel/articles/articles_list.html'
    permission_required = ['article_module.view_article']

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


class ArticleEditView(PermissionRequiredMixin, UpdateView):
    model = Article
    template_name = 'admin_panel/articles/edit_article.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_articles')
    permission_required = ['article_module.change_article']
    raise_exception = True
    permission_denied_message = 'شما دسترسی به این صفحه ندارید!'
