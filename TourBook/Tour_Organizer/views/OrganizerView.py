from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet

from Advertiser.models.offers import OfferRequest
from ..serializers.TourOrganizerSerializer import TourOrganizerSerializer
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from Core.permissions.OrganizerPermissions import IsOrganizerOwnerProfile


from django.core import exceptions


from drf_spectacular.utils import extend_schema_view, extend_schema

from ..services.SentimentAnalysis import get_organizer_tours_rating
from ..services.OrganizerStatistics import OrganizerStatistics


@extend_schema_view(
    list=extend_schema(
        summary="List of All Organizers who participate in Advertiser Offers", tags=["Organizers"]),
    retrieve=extend_schema(
        summary="Retrieve Organizer Profile", tags=["Organizer Profile"]),
    update_organizer=extend_schema(summary="Update Organizer Data",
                                   tags=["Organizer Profile"]),
)
class TourOrganizerView(UserViewSet):
    serializer_class = UserSerializer
    organizer_serializer_class = TourOrganizerSerializer
    permission_classes = [IsOrganizerOwnerProfile]

    def list(self, request):
        # get organziers who subscripe in advertisers offers
        try:
            advertiser = request.user.advertiser
            offers = advertiser.offers.all()
            offer_requests = OfferRequest.objects.filter(
                offer_object__in=offers, status='A'
            ).select_related('offer_point', 'offer_point__tour_object', 'offer_point__tour_object__tour_organizer')

            organizers = set()
            for offer_request in offer_requests:
                organizers.add(
                    offer_request.offer_point.tour_object.tour_organizer)

            serializer = self.organizer_serializer_class(
                list(organizers), many=True)
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request):
        """
        Retrieve the organizer data by id.

        This method returns the serialized data of the TourOrganizer instance associated with the authenticated user.
        It checks if all fields in the serialized data have a value (not None) and sets the data_status accordingly.

        Returns:
            Response: Serialized data of the organizer and status indicating the data_status.
        """
        try:
            organizer = request.user.organizer
            serializer = self.organizer_serializer_class(organizer)

            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Orgnaizer does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False)
    def update_organizer(self, request):
        """
        Update the organizer data by id.

        This method allows updating the user and organizer data associated with the authenticated user.
        It performs partial updates on the user and organizer instances based on the provided request data.

        Args:
            id (int) : id of the organizer
            request (Request): The HTTP request containing the updated user and organizer data.
            request contain to dictionaries :
                user => contain user data [phone , email , username] for updating and send email when user change his email
                organizer => contain organizer data [address , evaluation , situation , logo]

        Returns:
            Response: Serialized data of the updated organizer or error response if validation or update fails.
        """
        try:
            user = request.user
            organizer = user.organizer
            user_serializer = self.serializer_class(user)
            organizer_serializer = self.organizer_serializer_class(organizer)
            errors = []

            # don't forget to apply SRP
            if 'user' in request.data and request.data['user']:
                user_serializer = self.serializer_class(
                    user, data=request.data['user'], partial=True)
                if not user_serializer.is_valid(raise_exception=False):
                    errors.append(user_serializer.errors)
                else:
                    self.perform_update(user_serializer)

            if 'organizer' in request.data:
                organizer_serializer = self.organizer_serializer_class(
                    organizer, data=request.data['organizer'], partial=True)
                if not organizer_serializer.is_valid(raise_exception=False):
                    errors.append(organizer_serializer.errors)
                else:
                    organizer_serializer.save()

            if 'logo' in request.data:
                organizer_serializer = self.organizer_serializer_class(
                    organizer, data=request.data, partial=True)
                if not organizer_serializer.is_valid():
                    errors.append(organizer_serializer.errors)
                else:
                    organizer_serializer.save()

            if errors:
                raise ValidationError(errors)

            return Response(
                {
                    'data': organizer_serializer.data,
                    'message': 'Organizer Updated Successfully'
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Orgnaizer does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(

    list=extend_schema(summary="Get All Organizer Statstics",
                       tags=["Organizer Statistics"]),

)
class OrganizerStatisticsView(ModelViewSet):
    def list(self, request):
        # Applying SRP by separating concerns into smaller methods
        try:
            organizer = request.user.organizer
            tours = organizer.organizer_tours.filter(posted=1).all()

            organizer_statistics = OrganizerStatistics()
            result = organizer_statistics.get_tour_statistics(tours)
            organizer_tours_rating = get_organizer_tours_rating(tours)

            data = {
                "tour_per_months": result,
                "organizer_tours_rating": organizer_tours_rating
            }

            return Response({"data": data}, status=status.HTTP_200_OK)
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
