from django.shortcuts import render
from rest_framework import viewsets
from .models import Flight, Reservation
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from rest_framework.permissions import IsAdminUser   # Artık bunu permissionsda kullandık. Aslında burada çağırmaya gerek yok
from .permissions import IsStafforReadOnly

# Create your views here.

class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes =(IsStafforReadOnly,)
    
    def get_serializer_class(self):     # serializer_class a ait bu functionu override ederek istediğimiz kullanıcıya istediğimiz serializerı kullandıracağız
        serializer= super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer
    

class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user= self.request.user)
    
# class ReservationView(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
    
#     def get_queryset(self):      # bu override ile admin (is_staff) tüm reservasyonları, reservasyonu yapan ise yalnız kendi reservasyonunu görecek.
#         queryset = super().get_queryset()
#         if self.request.user.is_staff:    # view içinde 'self.request.user' deyip istek yapan kullanıcıya ulaşabiliyoruz. serializers içinde ise 'self.context["request"].user' dememiz gerekiyor.
#             return queryset
#         return queryset.filter(user=self.request.user)

    