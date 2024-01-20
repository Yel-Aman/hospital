from django.db import models

# class Item(models.Model):
#     name = models.CharField(max_length=256)
#     description = models.TextField()
#     price = models.FloatField()

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')])
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# New model from lesson 13
class Schedule(models.Model):
    timestamp_start = models.DateTimeField()
    timestamp_end = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name="schedules")

class Visit(models.Model):
    PLANNED = 'PLANNED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

    STATUSES_CHOICES = [
        (PLANNED,PLANNED),
        (COMPLETED,COMPLETED),
        (CANCELLED,CANCELLED)
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='visits')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUSES_CHOICES)
    notes = models.TextField(null=True, blank=True)
    schedule = models.ForeignKey(Schedule, null=True, on_delete=models.SET_NULL, related_name="visits")
    # schedule = models.OneToOneField(Schedule, null=True, on_delete=models.SET_NULL, related_name="visits")
    rating = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'{self.doctor.full_name} - {self.patient.full_name} - {self.visit_date_time}'

# HERE STARTS LESSON 13

