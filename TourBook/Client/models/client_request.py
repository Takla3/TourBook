from django.db import models
from .client import Client
from Core.models.base import BaseModel
from Tour_Organizer.models import Tour
import re


class SituationChoices(models.TextChoices):
    """
    A set of choices representing the situation options for a client request.

    Choices:
        PAID: Paid
        WAITING: Waiting
    """
    WAITING = "W", "Waiting"
    ACCEPTED = "A", "Accepted"
    REJECTED = "R", "Rejected"
    """
        Get a list of all possible values for the situation choices.

        Returns:
            List[str]: A list of all possible values for the situation choices.
    """

    def get_setuation_keys():
        keys = [key for key, _ in SituationChoices.choices]
        return keys


class ClientRequest(BaseModel):
    """
    Represents a client request for a tour.
    Fields:
        seat_num (IntegerField): The number of seats requested.
        situation (CharField): The situation of the client request.
        client_object (ForeignKey): The associated client object for the request.
        tour (ForeignKey): The associated tour for the request.
    Inherits From:
        Base: The base model providing common fields and functionality.
    """

    seat_num = models.IntegerField(default=0)

    situation = models.CharField(
        max_length=25, choices=SituationChoices.choices, default=SituationChoices.WAITING)

    client_object = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client_requests")

    tour_object = models.ForeignKey(
        Tour, on_delete=models.CASCADE, related_name='tour_requests')

    def clean(self):
        """
        Perform custom validation and data cleaning for the ClientRequest model.

        Raises:
            ValueError: If the seat_num field is not a positive integer or the situation is not a valid choice.
        """
        if not bool(re.match('^[0-9]{1,}$', str(self.seat_num))):
            raise ValueError(f"Seat num must be Number")
        if self.situation not in SituationChoices.get_setuation_keys():
            raise ValueError(
                f"situation should be  {' or '.join(SituationChoices.get_setuation_keys())}")

    def __str__(self):
        """
        Return a string representation of the ClientRequest object.

        Returns:
            str: A string representation of the ClientRequest object.
        """
        return f"ClientRequest #{self.client_object}"
