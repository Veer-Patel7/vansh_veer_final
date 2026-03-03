from __future__ import annotations
from django.utils import timezone
from decimal import Decimal
from datetime import date
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .models import Hotel, RoomType, Offer

class PricingEngine:
    """
    Centralized pricing engine to calculate discounts and final booking prices.
    Uses a strategy-based approach to apply auto-offers and coupons.
    """
    
    @staticmethod
    def calculate_price(hotel: Hotel, room_type: RoomType, check_in: date, check_out: date, 
                        coupon_code: str = None, user=None) -> dict:
        """
        Calculates the final price breakdown for a booking.
        
        Args:
            hotel: The Hotel instance.
            room_type: The RoomType instance.
            check_in: Check-in date.
            check_out: Check-out date.
            coupon_code: Optional coupon string.
            user: The User instance for per-user limit checks.
            
        Returns:
            A dictionary containing the base price, discounts, final price, tax, and grand total.
        """
        nights = (check_out - check_in).days
        if nights <= 0:
            nights = 1
            
        base_price = Decimal(str(room_type.price_per_night)) * nights
        total_discount = Decimal(0)
        applied_offers = []
        
        # 1. Fetch all potential offers for this hotel
        # Note: We consider APPROVED, SCHEDULED, and LIVE 
        # because a SCHEDULED offer might now be LIVE based on time.
        now = timezone.now()
        potential_offers = hotel.offers.filter(
            status__in=['APPROVED', 'SCHEDULED', 'LIVE']
        )
        
        # 2. Categorize offers: Auto-apply vs Coupon-only
        auto_offers = []
        coupon_offers = []
        
        for offer in potential_offers:
            # On-the-fly status check to ensure we only apply currently valid ones
            current_status = offer.update_status()
            if current_status == 'LIVE':
                if not offer.coupon_code:
                    auto_offers.append(offer)
                elif coupon_code and offer.coupon_code == coupon_code:
                    coupon_offers.append(offer)
        
        # 3. Logic: Apply Auto-offers first (checking stackability)
        for offer in sorted(auto_offers, key=lambda x: x.discount_value, reverse=True):
            if PricingEngine._is_eligible(offer, room_type, nights, base_price, check_in, user):
                discount = PricingEngine._get_discount_amount(offer, base_price)
                total_discount += discount
                applied_offers.append({
                    'id': offer.id,
                    'name': offer.name,
                    'amount': float(discount),
                    'type': offer.offer_type
                })
                if not offer.is_stackable:
                    break 
        
        # 4. Apply Coupon Offer
        coupon_discount = Decimal(0)
        if coupon_offers:
            offer = coupon_offers[0]
            if PricingEngine._is_eligible(offer, room_type, nights, base_price, check_in, user):
                # Ensure coupon can stack with auto-offers if stackable=True, 
                # or if total_discount is 0
                if offer.is_stackable or total_discount == 0:
                    discount = PricingEngine._get_discount_amount(offer, base_price)
                    coupon_discount = discount
                    total_discount += discount
                    applied_offers.append({
                        'id': offer.id,
                        'name': offer.name,
                        'amount': float(discount),
                        'type': 'COUPON'
                    })

        final_price = max(base_price - total_discount, Decimal(0))
        tax = final_price * Decimal('0.12') # Example 12% tax
        grand_total = final_price + tax
        
        return {
            'base_price': float(base_price),
            'discount': float(total_discount),
            'coupon_discount': float(coupon_discount),
            'final_price': float(final_price),
            'tax': float(tax),
            'grand_total': float(grand_total),
            'applied_offers': applied_offers,
            'nights': nights,
            'savings': float(total_discount),
            'check_in': check_in,
            'check_out': check_out
        }

    @staticmethod
    def _is_eligible(offer: Offer, room_type: RoomType, nights: int, base_price: Decimal, 
                     check_in: date, user=None) -> bool:
        """Internal helper to check if an offer applies to a specific context."""
        now = timezone.now()
        today = now.date()

        # Status & Date overlap check (redundant but safe)
            
        if nights < offer.min_nights:
            return False
        
        if offer.max_nights and nights > offer.max_nights:
            return False
            
        if base_price < offer.min_amount:
            return False
            
        # Applicability Check
        if offer.applicability == 'CATEGORY':
            if str(room_type.id) not in [str(x) for x in offer.room_categories]:
                # Fallback to name match
                if room_type.room_category_name not in offer.room_categories:
                    return False
        
        # Weekday check
        if offer.applicable_days:
            if check_in.weekday() not in offer.applicable_days:
                return False

        # Usage limits
        if offer.max_usage > 0 and offer.redemption_count >= offer.max_usage:
            return False
            
        # Advance booking & Last minute
        days_ahead = (check_in - today).days
        if offer.advance_booking_days > 0 and days_ahead < offer.advance_booking_days:
            return False
        if offer.last_minute_window > 0 and days_ahead > offer.last_minute_window:
            return False
            
        return True

    @staticmethod
    def _get_discount_amount(offer: Offer, base_price: Decimal) -> Decimal:
        """Calculates the absolute discount amount for an offer."""
        discount = Decimal(0)
        if offer.discount_type == 'PERCENT':
            discount = (base_price * Decimal(str(offer.discount_value))) / Decimal('100')
        else:
            discount = Decimal(str(offer.discount_value))
            
        # Apply Cape
        if offer.max_discount_limit and discount > offer.max_discount_limit:
            discount = Decimal(str(offer.max_discount_limit))
            
        return min(discount, base_price)
