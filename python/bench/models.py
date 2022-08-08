from django.db import models
from mongoengine import connect,Document,StringField,DynamicField,DateTimeField
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

connect(host="mongodb://192.168.57.119:27017/session")

class PgSession(models.Model):
    class Meta:
        db_table = 'session'
    token = models.CharField(max_length=512,primary_key=True)
    data = models.JSONField()
    expired_at = models.DateTimeField()
    
class MySession(models.Model):
    class Meta:
        db_table = 'my_session'
        
    token = models.CharField(max_length=512,primary_key=True)
    data = models.CharField(max_length=8192)
    expired_at = models.DateTimeField()
    
class MgSession(Document):
    token = StringField(primary_key=True)
    data = DynamicField()
    expired_at = DateTimeField()
    
class CaSession(DjangoCassandraModel):
    token = columns.Text(primary_key=True)
    data = columns.Text()
    expired_at = columns.DateTime()