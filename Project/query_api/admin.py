from django.contrib import admin

from query_api.models import Query

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    """Admin class for Query model"""

    list_display = ['id','cadastral_number','latitude','longtitude','result','created_at','updated_at']
    list_filter = ['result','updated_at']


