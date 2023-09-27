from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Request handlers
def captureKeyEvent(request):
    if request.method == 'GET':
        return render(request, 'hello.html', {'name': 'Silas'})
    if request.method == 'POST':
        key = request.POST.get('key')
        event = request.POST.get('event')
        print(key, event)
        return JsonResponse({'message': 'Key event captured',
                             'key': key,
                             'event': event})
    
    return JsonResponse({'error': 'Invalid Key'}, status=400)