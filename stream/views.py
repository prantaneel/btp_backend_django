from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })
def get_stream(request, node_id):
    # we will get the chatbox name from the url
    return render(request, "stream.html", {"node_id": node_id})