from jsonschema.exceptions import ValidationError
from rest_framework import serializers

# from .models import Item
from .models import Doctor, Patient, Visit, Schedule


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = '__all__'

class DoctorListSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    contact_info = serializers.CharField()

class DoctorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specialization','contact_info']

# class PatientListSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     full_name = serializers.CharField()
#     date_of_birth = serializers.DateField()
#     gender = serializers.CharField()


# FROM HERE for PATIENT

class PatientListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    date_of_birth = serializers.DateField()
    gender = serializers.CharField()

class PatientDetailedSerializer(PatientListSerializer):
    contact_info = serializers.CharField()

class PatientCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

# HERE STARTS LESSON 13

class VisitCreateSerializer(serializers.ModelSerializer):
    # schedule_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Schedule.objects.all(),
    #     read_only=True
    # )
    def validate_schedule(self, value):
        visit_count = value.visit.count()
        if 3 <= value.visits.count():
            raise ValidationError ("too many reserves on that time")
        return value
    class Meta:
        model = Visit
        fields = ['patient','doctor','service', 'schedule_id']

class ScheduleSerializer(serializers.ModelSerializer):
    def validate(self,attrs):
        attrs = super().validate(attrs)

        timestamp_start, timestamp_end = attrs['timestamp_start'], attrs['timestamp_end']

        exists = Schedule.objects.filter(
            timestamp_start__lte = timestamp_start,
            timestamp_end__gde = timestamp_start
        ).exists()

        if exists:
            raise ValidationError('something wrong Yela')


class VisitRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=0, max_value=10)
    class Meta:
        model = Visit
        fields = ['rating']