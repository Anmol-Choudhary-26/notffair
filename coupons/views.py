from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from coupons.models import Coupon, ClaimedCoupon
from coupons.serializers import CouponSerializer, ClaimedCouponSerializer


# based on https://djangosnippets.org/snippets/1703/

# def group_required(*group_names):
#     """Requires user membership in at least one of the groups passed in."""
#     def in_groups(u):
#         if u.is_authenticated():
#             if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
#                 return True
#         return False
#     return user_passes_test(in_groups)

def get_redeemed_queryset(user, coupon_id=None):
    """
    Return a consistent list of the redeemed list.  across the two endpoints.
    """

    api_command = 'REDEEMED'

    # If the a coupon isn't specified, get them all.
    if coupon_id is None:
        qs_all = ClaimedCoupon.objects.all()
        qs_some = ClaimedCoupon.objects.filter(user=user.id)
    else:
        qs_all = ClaimedCoupon.objects.filter(coupon=coupon_id)
        qs_some = ClaimedCoupon.objects.filter(coupon=coupon_id, user=user.id)

    if user.is_superuser:
        return qs_all

    
    return qs_some


class CouponViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets you create, delete, retrieve coupons.
    """

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    
    search_fields = ('code', 'code_l')
    serializer_class = CouponSerializer

    def get_queryset(self):
        """
        Return a subset of coupons or all coupons depending on who is asking.
        """

        api_command = 'LIST'
        qs_all = Coupon.objects.all()
        # qs_some = Coupon.objects.filter( user=self.request.user.id)

       
        return qs_all

      
        

    # @method_decorator(group_required('CREATE'))
    def create(self, request, **kwargs):
        """
        Create a coupon
        """

        serializer = CouponSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        """
        Delete the coupon.
        """

        coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
        coupon.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None, **kwargs):
        """
        Anybody can retrieve any coupon.
        """

        value_is_int = False

        try:
            pk = int(pk)
            value_is_int = True
        except ValueError:
            pass

        if value_is_int:
            coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
        else:
            coupon = get_object_or_404(Coupon.objects.all(), code_l=pk.lower())

        serializer = CouponSerializer(coupon, context={'request': request})

        return Response(serializer.data)

    # @method_decorator(group_required('UPDATE'))
    def update(self, request, pk=None, **kwargs):
        """
        This forces it to return a 202 upon success instead of 200.
        """

        coupon = get_object_or_404(Coupon.objects.all(), pk=pk)

        serializer = CouponSerializer(coupon, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def redeemed(self, request, pk=None, **kwargs):
        """
        Convenience endpoint for getting list of claimed instances for a coupon.
        """

        coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
        qs = get_redeemed_queryset(self.request.user, coupon.id)

        serializer = ClaimedCouponSerializer(qs, many=True, context={'request': request})

        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def redeem(self, request, pk=None, **kwargs):
        """
        Convenience endpoint for redeeming.
        """

        queryset = Coupon.objects.all()
        coupon = get_object_or_404(queryset, pk=pk)

        # Maybe should do coupon.redeem(user).
        # if data['expires'] < now():

        data = {
            'coupon': pk,
            'user':   self.request.user.id,
        }

        serializer = ClaimedCouponSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            
            serializer.save()
            

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimedCouponViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets you retrieve claimed coupon details.
    """

    serializer_class = ClaimedCouponSerializer

    def get_queryset(self):
        return get_redeemed_queryset(self.request.user)

    def create(self, request,pk=None, **kwargs):
       
        
        return Response(status=status.HTTP_404_NOT_FOUND)

    # @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        """
        Basically un-redeem a coupon.
        """

        redeemed = get_object_or_404(ClaimedCoupon.objects.all(), pk=pk)
        redeemed.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

