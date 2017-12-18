from django.shortcuts import render,render_to_response

# Create your views here.

def index(request):
    login_status=request.session.get('login_status')
    if login_status:
        account=request.session.get('account')
        return render_to_response('front_index.html',{'account':account})
    else:
        return render_to_response('front_index.html')
