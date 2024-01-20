from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Doctor, Patient
from .serializers import DoctorListSerializer, DoctorRetrieveSerializer, DoctorCreateSerializer, DoctorUpdateSerializer, \
    PatientListSerializer, PatientDetailedSerializer, PatientCreateOrUpdateSerializer
from .permissions import DoctorAccessPermission, RoleBasedPermissionsMixin, HasPermissionByAuthenticatedUserRole
from django_filters.rest_framework import DjangoFilterBackend
from .filter import DoctorFilterSet
from rest_framework import filters

# from .models import Item
# from .serializers import ItemSerializer
# class ItemListCreateView(generics.ListCreateAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer

class DoctorView(viewsets.GenericViewSet,
                 RoleBasedPermissionsMixin, #Lesson 12 for each action own permission
                 mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin):
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DoctorAccessPermission, HasPermissionByAuthenticatedUserRole]

    filter_backends = [DjangoFilterBackend, ] #lesson12.1
    filterset_fields = ['first_name', 'last_name','specialization']
    filterset_class = DoctorFilterSet #eta stroka perepisyvaet stroku sverhu

    # pagination_class = [CustomPagination]

    def get_action_permission(self):  #lesson 12
        if self.action in ('list','retrieve'):
            self.action_permission = ['view_doctor', ]
        elif self.action_permission == 'list_patient':
            self.action_permission = ['view_patient']
        else:
            self.action_permission = []

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        if self.action == 'retrieve':
            return DoctorRetrieveSerializer
        if self.action == 'create':
            return DoctorCreateSerializer
        if self.action == 'update':
            return DoctorUpdateSerializer
        if self.action == 'list_patient':
            return PatientListSerializer

    def get_queryset(self):
        if self.action == 'list_patient':
            return Patient.objects.all()

        return Doctor.objects.all()

    def list_patient(self,request,id):
        queryset = self.get_queryset().filter(visits__doctor_id=id)

        serializer = self.get_serializer(queryset, many =True)

        return Response(data=serializer.data)

# FROM HERE H/W 12 View For model Patient

class PatientView(viewsets.GenericViewSet,
                 RoleBasedPermissionsMixin,
                 mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin):
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DoctorAccessPermission, HasPermissionByAuthenticatedUserRole]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender']
    search_filed = ['first_name','last_name']

    def get_action_permission(self):
        if self.action in ('list','retrieve'):
            self.action_permission = ['view_patient', ]
        elif self.action == 'create':
            self.action_permission = ['add_patient']
        elif self.action == 'update':
            self.action_permission = ['change_patient']
        elif self.action == 'destroy':
            self.action_permission = ['delete_patient']


    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        if self.action == 'retrieve':
            return PatientDetailedSerializer
        if self.action == 'create':
            return PatientCreateOrUpdateSerializer
        if self.action == 'update':
            return PatientCreateOrUpdateSerializer

    def get_queryset(self):
        return Patient.objects.all()

    def list_patient(self,request,id):
        queryset = self.get_queryset().filter(visits__doctor_id=id)

        serializer = self.get_serializer(queryset, many =True)

        return Response(data=serializer.data)
