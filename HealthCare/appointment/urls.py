from appointment.views import (
    hello,
    list_treatments,
    png_visual,
    create_treatment,
    appt_view,
    update_appt,
    ClinicApiView,
    AppointmentViewset,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# creating the routers
router = DefaultRouter()

router.register(r"appointment", AppointmentViewset, basename="appointment")

urlpatterns = [
    path("hello/", hello, name="hello"),
    path("treatments/", list_treatments, name="list_treatments"),
    path("visual/", png_visual, name="png_visual"),
    path("create_treatment/", create_treatment, name="create_treatment"),
    path("appt/", appt_view, name="appt_view"),
    path("appt/<int:id>/", update_appt, name="update_appt"),
    path("clinic/", ClinicApiView.as_view(), name="clinic_api"),
    path("clinic/<int:id>", ClinicApiView.as_view(), name="clinic_api"),
    path("", include(router.urls)),
]
