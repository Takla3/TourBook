from datetime import datetime
from rest_framework import serializers
from Tour_Organizer.models.tour_point import TourPoint
from Tour_Organizer.models.tour import Tour
from Advertiser.models.offers import Offer
from Advertiser.serializers.OfferRequestSerializer import OfferRequestSerializer
import re
from Core.helpers.helpers import is_within
from django.core import exceptions


class TourPointSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    offer_request = OfferRequestSerializer()

    class Meta:
        model = TourPoint
        fields = (
            'id',
            'title',
            'position',
            'description',
            'arrival_time',
            'leaving_time',
            'axis_x',
            'axis_y',
            'offer_request',
            'status'
        )
        extra_kwargs = {
            "tour_object": {
                "write_only": True
            }
        }

    def get_status(self, tour_point):
        status = tour_point.offer_request.status
        return status

    def get_char_fields(self):
        char_fields = []
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.CharField):
                char_fields.append(field_name)

        return char_fields

    def get_numeric_fields(self):
        numeric_fields = []
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.IntegerField) or isinstance(field, serializers.DecimalField):
                numeric_fields.append(field_name)

        return numeric_fields

    def validate(self, attrs):
        """
        Validate the TourPoint attribute.

        - Check if arrival_time and leaving_time are in the future.
        - Check if leaving_time is after arrival_time.
        - Ensure axis_x and axis_y are within the specified range.
        - Ensure numeric values expect axis_x and axis_y are non-negative.
        """
        errors = {}
        attrs = super().validate(attrs)
        date_fields = ['leaving_time', 'arrival_time']
        date_errors = []
        for field in date_fields:
            if field in attrs:
                if attrs[field] < datetime.now():
                    date_errors.append(
                        "Arrive Time or Leaving Time can't be in the past")

        if 'leaving_time' in attrs and 'arrival_time' in attrs:
            if attrs['arrival_time'] >= attrs['leaving_time']:
                date_errors.append(
                    "Leaving Time can't be before Arrive Time!!")
        if len(date_errors) > 0:
            errors['date'] = date_errors

        for field in self.get_numeric_fields():
            if attrs.get(field) is not None:
                if field in ['axis_x', 'axis_y']:
                    if not is_within(-90, 180, attrs[field]):
                        errors[field] = f"{field} Must be between -90 and 180"
                else:
                    if attrs[field] < 0:
                        errors[field] = f"{field} Should NOT be Negative"

        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        offer_request_data = validated_data.pop('offer_request')
        offer = Offer.objects.get(pk=offer_request_data['offer_object'])
        offer_request_serializer = OfferRequestSerializer(
            data=offer_request_data)
        if not offer_request_serializer.is_valid():
            raise exceptions.ValidationError(offer_request_serializer.errors)
        offer_request = offer_request_serializer.save(offer_object=offer)

        tour_point = TourPoint.objects.create(
            offer_request=offer_request, **validated_data)
        return tour_point
