from rest_framework import serializers
from .models import Flight, Reservation, Passenger


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines", 
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
        )



class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"
        
        
    
class ReservationSerializer(serializers.ModelSerializer):
    
    passenger = PassengerSerializer(many=True, required = True)
    flight = serializers.StringRelatedField()       # flight modelinde tanımlı __str__ gelir 
    flight_id = serializers.IntegerField()
    user = serializers.StringRelatedField()  #user modelinde tanımlı __str__ gelir
    
    class Meta:
        model = Reservation
        fields = ("id", "flight", "flight_id", "user", "passenger")
        
    def create(self, validated_data):
        passenger_data = validated_data.pop("passenger")       #passenger bilgisini buradan çıkardım. Her bir passenger bilgisini aşağıda for döngüsü ile create edip sonra tekrar reservation ile birleştireceğim
        validated_data["user_id"]=self.context["request"].user.id    # user id!sini bu yolla validated_data içine atıyorum
        reservation = Reservation.objects.create(**validated_data)
        
        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation

    
class StaffFlightSerializer(serializers.ModelSerializer):
    
    reservation = ReservationSerializer(many=True, read_only = True)   # Bu sayede staff personeli bir uçuşa ait tüm rezervasyonları da görebilecek, ama read_only=True ile yeni flight oluşturulurken rezervasyon oluşturmak zorunda kalmayacak
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines", 
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
            "reservation",
        ) 


   # veya
    # class Meta:
    #     model = Reservation
    #     fields = "__all__"