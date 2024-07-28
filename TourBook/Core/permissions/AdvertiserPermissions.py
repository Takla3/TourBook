from rest_framework import permissions
from django.contrib.auth import get_user_model
from ..models.user import Role

from Advertiser.models.advertiser import Advertiser

from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


class IsAdvertiserOwnerProfile(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.ADVERTISER:
                    if request.method == "POST":
                        return True
                    try:
                        advertiser = Advertiser.objects.get(
                            pk=view.kwargs['advertiser_id'])
                        return advertiser == request.user.advertiser
                    except ObjectDoesNotExist:
                        return True