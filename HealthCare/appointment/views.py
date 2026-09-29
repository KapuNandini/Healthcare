from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from appointment.models import TreatmentPlan, Appointments, Clinic
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from appointment.serializers import AppointmentSerializer
from rest_framework.viewsets import ModelViewSet

# importing csrf_exempt from django


# Create your views here.
def hello(request):
    return HttpResponse("Hello World from appointment app ")


def list_treatments(request):
    treatments = TreatmentPlan.objects.all()
    treatment_list = []
    for treatment in treatments:
        treatment_list.append(
            {
                "id": treatment.id,
                "name": treatment.PlanName,
                "description": treatment.Description,
                "Prescriptions": treatment.Prescriptions,
                "Price": treatment.Price,
            }
        )
    return JsonResponse(treatment_list, safe=False)


def png_visual(request):
    # Create a FileResponse object to serve the PNG file
    file_path = "sample.png"  # Replace with the actual path to your PNG file
    response = FileResponse(open(file_path, "rb"), content_type="image/png")
    response["Content-Disposition"] = (
        'inline; filename="image.png"'  # Optional: specify filename
    )
    return response


# Types of requests
@csrf_exempt
def create_treatment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("received payload  ", data)
        treatment = TreatmentPlan.objects.create(
            PlanName=data.get("PlanName"),
            Description=data.get("Description"),
            Prescriptions=data.get("Prescriptions"),
            Price=data.get("Price"),
        )
        return JsonResponse(
            {
                "id": treatment.id,
                "PlanName": treatment.PlanName,
                "Description": treatment.Description,
                "Prescriptions": treatment.Prescriptions,
                "Price": treatment.Price,
            }
        )
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)


@api_view(["GET", "POST"])
def appt_view(request):
    if request.method == "GET":
        appointments = Appointments.objects.all()
        appointment_list = []
        for appointment in appointments:
            appointment_list.append(
                {
                    "id": appointment.id,
                    "PatientName": appointment.PatientName,
                    "PatientEmail": appointment.PatientEmail,
                    "PatientPhone": appointment.PatientPhone,
                    "AppointmentDate": appointment.AppointmentDate,
                    "TreatmentPlan": appointment.TreatmentPlan.PlanName,
                }
            )
        return Response(appointment_list)

    elif request.method == "POST":
        data = request.data
        treatment_plan_id = data.get("TreatmentPlan")
        try:
            treatment_plan = TreatmentPlan.objects.get(id=treatment_plan_id)
        except TreatmentPlan.DoesNotExist:
            return Response({"error": "Treatment plan not found."}, status=404)

        appointment = Appointments.objects.create(
            PatientName=data.get("  "),
            PatientEmail=data.get("PatientEmail"),
            PatientPhone=data.get("PatientPhone"),
            AppointmentDate=data.get("AppointmentDate"),
            TreatmentPlan=treatment_plan,
        )
        return Response(
            {
                "id": appointment.id,
                "PatientName": appointment.PatientName,
                "PatientEmail": appointment.PatientEmail,
                "PatientPhone": appointment.PatientPhone,
                "AppointmentDate": appointment.AppointmentDate,
                "TreatmentPlan": appointment.TreatmentPlan.PlanName,
            }
        )


@api_view(["GET", "PUT", "DELETE"])
def update_appt(request, id):
    try:
        appointment = Appointments.objects.get(id=id)
    except Appointments.DoesNotExist:
        return Response({"error": "Appointment not found."}, status=404)

    if request.method == "PUT":
        data = request.data
        treatment_plan_id = data.get("TreatmentPlan")
        try:
            treatment_plan = TreatmentPlan.objects.get(id=treatment_plan_id)
        except TreatmentPlan.DoesNotExist:
            return Response({"error": "Treatment plan not found."}, status=404)

        appointment.PatientName = data.get("PatientName", appointment.PatientName)
        appointment.PatientEmail = data.get("PatientEmail", appointment.PatientEmail)
        appointment.PatientPhone = data.get("PatientPhone", appointment.PatientPhone)
        appointment.AppointmentDate = data.get(
            "AppointmentDate", appointment.AppointmentDate
        )
        appointment.TreatmentPlan = treatment_plan
        appointment.save()

        return Response(
            {
                "id": appointment.id,
                "PatientName": appointment.PatientName,
                "PatientEmail": appointment.PatientEmail,
                "PatientPhone": appointment.PatientPhone,
                "AppointmentDate": appointment.AppointmentDate,
                "TreatmentPlan": appointment.TreatmentPlan.PlanName,
            }
        )

    elif request.method == "DELETE":
        appointment.delete()
        return Response({"message": "Appointment deleted successfully."})
    elif request.method == "GET":
        return Response(
            {
                "id": appointment.id,
                "PatientName": appointment.PatientName,
                "PatientEmail": appointment.PatientEmail,
                "PatientPhone": appointment.PatientPhone,
                "AppointmentDate": appointment.AppointmentDate,
                "TreatmentPlan": appointment.TreatmentPlan.PlanName,
            }
        )


class ClinicApiView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                clinic = Clinic.objects.get(id=id)
                data = {
                    "id": clinic.id,
                    "name": clinic.ClinicName,
                    "address": clinic.ClinicAddress,
                    "TreatmentPlans": [
                        tp.PlanName for tp in clinic.TreatmentPlans.all()
                    ],
                }
                return Response(data)
            except Clinic.DoesNotExist:
                return Response({"error": "Clinic not found."}, status=404)
        else:
            clinics = Clinic.objects.all()
            clinic_list = []
            for clinic in clinics:
                clinic_list.append(
                    {
                        "id": clinic.id,
                        "name": clinic.ClinicName,
                        "address": clinic.ClinicAddress,
                        "TreatmentPlans": [
                            tp.PlanName for tp in clinic.TreatmentPlans.all()
                        ],
                    }
                )
            return Response(clinic_list)

    def post(self, request, id=None):
        data = request.data
        # since Treatment plans is a many to many field we need to veriry
        treatment_plan_ids = data.get("TreatmentPlans", [])
        treatment_plans = TreatmentPlan.objects.filter(id__in=treatment_plan_ids)

        # creating part of the clinic
        clinic = Clinic.objects.create(
            ClinicName=data.get("ClinicName"),
            ClinicAddress=data.get("ClinicAddress"),
        )
        # clinic.set(treatment_plans)

        # returning the response
        return Response(
            {
                "ClinicName": data.get("ClinicName"),
                "ClinicAddress": data.get("ClinicAddress"),
                "TreatmentPlans": [tp.PlanName for tp in treatment_plans],
            }
        )

    def put(self, request, id=None):
        try:
            clinic = Clinic.objects.get(id=id)
        except Clinic.DoesNotExist:
            return Response({"error": "Clinic not found."}, status=404)

        data = request.data
        clinic.name = data.get("ClinicName", clinic.ClinicName)
        clinic.address = data.get("ClinicAddress", clinic.ClinicAddress)
        # clinic.phone = data.get("phone", clinic.phone)
        clinic.save()

        return Response(
            {
                "id": clinic.id,
                "ClinicName": clinic.name,
                "ClinicAddress": clinic.address,
                "TreatmentPlans": [tp.PlanName for tp in clinic.TreatmentPlans.all()],
            }
        )

    def delete(self, request, id=None):
        try:
            clinic = Clinic.objects.get(id=id)
        except Clinic.DoesNotExist:
            return Response({"error": "Clinic not found."}, status=404)

        clinic.delete()
        return Response({"message": "Clinic deleted successfully."})


class AppointmentViewset(ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
