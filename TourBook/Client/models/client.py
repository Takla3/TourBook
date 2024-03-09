from django.db import models
from django.conf import settings
from .base import Base 
import re 

class GenderChoices(models.TextChoices):
     """
     A set of choices for representing gender options.

     Choices:
        MALE: Male
        FEMALE: Female
     """
     MALE="M","Male"
     FEMALE="F","Female"    

     def get_values():
        """
        Get a list of valid gender choices.

        Returns:
            List[str]: A list of valid gender choices.
        """
        gender_choices = [key for key,_ in GenderChoices.choices]
        return gender_choices
class Client(Base):
        
    """
       Represents a client in the system.

       Fields:
        first_name (CharField): The first name of the client.
        middle_name (CharField): The middle name of the client (optional).
        last_name (CharField): The last name of the client.
        birth_date (DateTimeField): The birth date of the client.
        gender (CharField): The gender of the client.
        user (OneToOneField): The associated user account for the client.

       Inherits From:
        Base: The base model providing common fields and functionality.

       
    """
  
    first_name=models.CharField(max_length=255)
    middle_name=models.CharField(max_length=255 , null=True)
    last_name=models.CharField(max_length=255)
    birth_date=models.DateField()
    gender=models.CharField(max_length=1, choices=GenderChoices.choices)
    user=models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)



    def clean(self):
        """
        Perform custom validation and data cleaning for the Client model.

        Raises:
            ValueError: If any of the character fields do not match the regex pattern.
            ValueError: If the gender value is not one of the valid choices.
        """
        for field in self.get_char_fields():
            if not re.match('^[A-z0-9\s]{4,}$',getattr(self,field.name)):
                raise ValueError(f"{field.name} is invalid")

        if self.gender not in GenderChoices.get_values():
            raise ValueError(f"gender should be  {' or '.join(GenderChoices.get_values())}")

    def __str__(self):
        return "Client "+self.user.name