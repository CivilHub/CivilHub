from rest_framework import routers
import views

router = routers.DefaultRouter()

router.register('actstream', views.ActivityViewSet, 'actstream')
