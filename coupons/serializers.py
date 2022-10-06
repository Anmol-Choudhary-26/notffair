from django.apps import apps
from django.utils.timezone import now
from rest_framework import serializers

from coupons.models import Coupon, ClaimedCoupon


class CouponSerializer(serializers.ModelSerializer):
    """
    RW Coupon serializer.
    """

    def validate(self, data):
        """
        Verify the input used to create or update the coupon is valid. 
        """
       
        if 'value' in data and data['value'] > 1.0:
            raise serializers.ValidationError("Percentage discount specified greater than 100%.")

    
        # Verify the lowercase code is unique.
        # IntegrityError: UNIQUE constraint failed: coupons_coupon.code_l and not returning 400.
        qs = Coupon.objects.filter(code_l=data['code'].lower())
        if qs.count() > 0:
            # there was a matching one, is it this one?
            if self.instance:
                if data['code'].lower() != self.instance.code_l:
                    raise serializers.ValidationError("Coupon code being updated to a code that already exists.")
            else:
                raise serializers.ValidationError("Creating coupon with code that violates uniqueness constraint.")

        data['code_l'] = data['code'].lower()

        return data

    def validate_repeat(self, value):
        """
        Validate that if it's specified it can be -1, 1, or more than that, but not zero.
        """

        if value < 0:
            raise serializers.ValidationError("Repeat field can be 0 for infinite, otherwise must be greater than 0.")

        return value

    def create(self, validated_data):
        return Coupon.objects.create(**validated_data)

    class Meta:
        model = Coupon
        fields = ('coupon_name', 'created', 'updated', 'code',
                  'code_l',  'repeat',
                  'value', 'id')


class ClaimedCouponSerializer(serializers.ModelSerializer):
    """
    RW ClaimedCoupon serializer.
    """

    def validate(self, data):
        """
        Verify the coupon can be redeemed.
        """

        coupon = data['coupon']
        user = data['user']

        # Is the coupon redeemed already beyond what's allowed?
        redeemed = ClaimedCoupon.objects.filter(coupon=coupon.id, user=user.id).count()
        if coupon.repeat > 0:
            if redeemed >= coupon.repeat:
                # Already too many times (note: we don't update the claimed coupons, so this is a fine test).
                # Also, yes, > should never happen because the equals check will be hit first, but just in case
                # you somehow get beyond that... ;)
                raise serializers.ValidationError("Coupon has been used to its limit.")
      
        return data

    class Meta:
        model = ClaimedCoupon
        fields = ('redeemed', 'coupon', 'user', 'id')

