from django.db import models
from .user import UserAccount
from datetime import datetime


class Subscription (models.Model):
    """
    Model representing a subscription.

    Attributes:
        Start_Date (datetime): The start date and time of the subscription.
        End_Date (datetime): The end date and time of the subscription.
        Payment (Decimal): The payment associated with the subscription.
        user_id (UserAccount): The user associated with the subscription.
    """
    Start_Date = models.DateTimeField()
    End_Date = models.DateTimeField()
    Payment = models.DecimalField(max_length=15)
    user_id = models.ForeignKey( 
        UserAccount,
        on_delete = models.CASCADE 
        )
    def clean(self):
        """
        Performs validation on the model fields.

        Raises:
        - ValueError: If any of the validation conditions fail.
        """

        if self.start_date < datetime.now() or self.end_date < datetime.now():
            raise ValueError("Start Date or End Date can't be in the past")

        if self.start_date >= self.end_date:
            raise ValueError("End Date can't be before Start Date!!")
    def save(self, *args, **kwargs):
        """
        Overrides the save method to format the start and end dates into datetime objects.
        """
        self.end_date = datetime.strptime(
            str(self.end_date), "%Y-%m-%d %H:%M:%S")

        self.start_date = datetime.strptime(
            str(self.start_date), "%Y-%m-%d %H:%M:%S")