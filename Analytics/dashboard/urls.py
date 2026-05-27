from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from dashboard.views_louvain import louvain_network_tool




urlpatterns = [
    path('', views.index_view, name="dashboard"),
    path("tool/louvain-network/", louvain_network_tool, name="louvain_network_tool"),

    
    
    
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
