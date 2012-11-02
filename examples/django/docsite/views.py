from django.http import HttpResponse
from docstring.djangodoc import document

@document()
def bye(request):
    """
    Returns a 'bye <name>' response.

    @param name: str, [default: 'foo']
    """
    name = request.GET.get('name', 'foo')
    return HttpResponse("Bye %s" % name)

@document()
def hello(request):
    """
    Returns a 'hello <name>' response.

    @param name: str, [default: 'foo']
    """
    name = request.GET.get('name', 'foo')
    return HttpResponse("Hello %s" % name)
