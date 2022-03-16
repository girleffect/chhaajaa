from .models import BlogPage, BlogIndexPage
from django.shortcuts import render

def search(request):
    query_string = request.GET.get('query', None)

    # Parse query
    if query_string != None:
       queryset = BlogPage.objects.filter(title__icontains=query_string).live().distinct()
    else:
        queryset = None
    return render(request, 'blog/blog_index_search_page.html', {
        'blogindex': BlogIndexPage.objects.live().last(),
        'search_query': query_string,
        'blogpages': queryset,
    })