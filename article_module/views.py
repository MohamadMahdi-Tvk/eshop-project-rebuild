from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from article_module.models import Article


class ArticleListView(ListView):
    model = Article
    paginate_by = 5
    template_name = 'article_module/articles_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        return context



# class ArticleView(View):
#     def get(self, request):
#         articles = Article.objects.filter(is_active=True)
#         context = {
#             'articles': articles
#         }
#         return render(request, 'article_module/articles_page.html', context)
