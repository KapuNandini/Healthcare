from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from appointment.models import Appointments


class AppointmentSerializer(ModelSerializer):
    treatment = SerializerMethodField()

    def get_treatment(self, obj):
        return {
            "PlanName": obj.TreatmentPlan.PlanName,
            "Description": obj.TreatmentPlan.Description,
            "Prescriptions": obj.TreatmentPlan.Prescriptions,
            "Price": obj.TreatmentPlan.Price,
        }

    class Meta:
        model = Appointments
        fields = "__all__"
