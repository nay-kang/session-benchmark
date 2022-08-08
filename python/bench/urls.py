"""bench URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
import uuid
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse
import django
from bench.models import PgSession,MySession,MgSession,CaSession
from django.core.cache import cache
import json

SESSION_LIFETIME = 3600

def generate_token():
    return str(uuid.uuid4())

def generate_sample():
    code = str(uuid.uuid4())
    now = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "created_at":now,
        "cilent":'api_client',
        "scope":['database','image','file'],
        'refresh_code':code
    }
    return data

def get_session_expired_at():
    now = timezone.now()+timedelta(days=1)
    
    return now

def index(request):
    return HttpResponse(django.VERSION)

'''
create table my_session(
    token char(64) primary key,
    data varchar(2048) null,
    expired_at timestamp null
);
'''
def mysql(request):
    token = generate_token()
    data = generate_sample()
    expired_at = get_session_expired_at()
    
    #insert new session
    session = MySession(token=token,data=data,expired_at=expired_at)
    session.save(using='mysql')
    
    #find session
    session = MySession.objects.using('mysql').get(token=token)
    
    #update session
    expired_at = get_session_expired_at()
    MySession.objects.using('mysql').filter(token=token).update(data=data,expired_at=expired_at)
    
    return HttpResponse("")

'''
create table session(
    token text primary key,
    data jsonb null,
    expired_at timestamp null
);
'''
def postgresql(requset):
    token = generate_token()
    data = generate_sample()
    expired_at = get_session_expired_at()
    
    #insert new session
    session = PgSession(token=token,data=data,expired_at=expired_at)
    session.save(using='pg')
    
    #find session
    session = PgSession.objects.using('pg').get(token=token)
    
    #update session
    expired_at = get_session_expired_at()
    PgSession.objects.using('pg').filter(token=token).update(data=data,expired_at=expired_at)
    
    return HttpResponse("")

def redis(request):
    token = generate_token()
    data = generate_sample()
    
    #insert new session
    cache.set(token,data,SESSION_LIFETIME)
    
    #find session
    session = cache.get(token)
    
    #update session
    cache.set(token,data,SESSION_LIFETIME)
    
    return HttpResponse("")

def mongodb(requset):
    token = generate_token()
    data = generate_sample()
    expired_at = get_session_expired_at()
    
    #insert new session
    session = MgSession(token=token,data=data,expired_at=expired_at)
    session.save()
    
    #find session
    session = MgSession.objects(token=token)
    
    #update session
    expired_at = get_session_expired_at()
    MgSession.objects(token=token).update(data=data,expired_at=expired_at)
    
    return HttpResponse("")

'''
create table ca_session(
    "token" text primary key,
    data text,
    expired_at timestamp
);
'''
def cassandra(request):
    token = generate_token()
    data = generate_sample()
    expired_at = get_session_expired_at()
    
    #insert new session
    session = CaSession(token=token,data=json.dumps(data),expired_at=expired_at)
    session.save()
    
    #find session
    session = CaSession.objects.get(token=token)
    
    #update session
    expired_at = get_session_expired_at()
    CaSession.objects.filter(token=token).update(data=json.dumps(data),expired_at=expired_at)
    
    return HttpResponse("")

urlpatterns = [
    path('',index),
    path('postgresql',postgresql),
    path('mysql',mysql),
    path('redis',redis),
    path('mongodb',mongodb),
    path('cassandra',cassandra)
]