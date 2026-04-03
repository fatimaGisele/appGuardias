from rest_framework.routers import DefaultRouter
from views import RolView

router =  DefaultRouter
router.register(r'',RolView, basename="rol")

urlpatterns = router.urls