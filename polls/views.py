from django.http import HttpResponse

def index_view(request):
    return HttpResponse('Polls index page')
