from django.contrib import admin

# importing the model to register
from appointment.models import Appointments, Clinic, TreatmentPlan


class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        "PlanName",
        "Description",
        "Prescriptions",
    )

    search_fields = ("PlanName",)
    list_filter = ("PlanName",)
    # fieldset


# Register your models here.
admin.site.register(Appointments)
admin.site.register(Clinic)
admin.site.register(TreatmentPlan, TreatmentPlanAdmin)
