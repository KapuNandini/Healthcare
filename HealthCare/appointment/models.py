from django.db import models


class TreatmentPlan(models.Model):
    """generating treatment plan
    records to connect Appointments"""

    PlanName = models.CharField(max_length=70)
    Description = models.TextField(null=True)
    Prescriptions = models.TextField(null=True)
    Price = models.FloatField(null=True)

    # adding the record name
    def __str__(self):
        return self.PlanName

    @property
    def offerprice(self):
        """generating offer price for treatment plan"""
        offer = self.Price * 0.9
        return offer


class Appointments(models.Model):
    """generating appointments records to connect
    treatment plan and patient"""

    PatientName = models.CharField(max_length=70)
    PatientEmail = models.EmailField()
    PatientPhone = models.CharField(max_length=15)
    AppointmentDate = models.DateTimeField()
    TreatmentPlan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE)

    def __str__(self):
        return self.PatientName


class Clinic(models.Model):
    """
    a clinic must have many to many relationship with treatment plan
    one clinic has n number of treatment plan vice versa one treatment plan
    can be used in n number of clinics
    """

    ClinicName = models.CharField(max_length=70)
    ClinicAddress = models.TextField()
    TreatmentPlans = models.ManyToManyField(TreatmentPlan)

    def __str__(self):
        return self.ClinicName
