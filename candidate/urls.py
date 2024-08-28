from django.urls import path
from candidate import views
urlpatterns = [
     path('dash/',views.candidateHome,name='dash'),
     path('',views.Home,name='home'),
     path('applyjob/<int:id>/',views.applyJob,name='applyjob'),
     path('applylist/',views.myjoblist,name='mylist')
]
