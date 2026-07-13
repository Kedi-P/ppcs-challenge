"""PPCS-009: flag member-only prices advertised as general public prices."""
from app.main import PromoIn, validate
from app.rules import is_member_price_compliant


def test_member_only_advertised_as_public_is_non_compliant():
    assert is_member_price_compliant(member_only=True, display_channel="public") is False


def test_member_only_labelled_member_only_is_compliant():
    assert is_member_price_compliant(member_only=True, display_channel="member") is True


def test_public_offer_unaffected_by_rule():
    # A non-member offer is always compliant for this rule, even in a public channel.
    assert is_member_price_compliant(member_only=False, display_channel="public") is True


def test_validate_flags_member_only_as_public():
    response = validate(
        PromoIn(
            sku="SKU-M",
            was_price=10.00,
            now_price=9.00,
            member_only=True,
            display_channel="public",
        )
    )
    assert response["member_price_compliant"] is False


def test_validate_member_only_labelled_member_only_passes():
    response = validate(
        PromoIn(
            sku="SKU-M",
            was_price=10.00,
            now_price=9.00,
            member_only=True,
            display_channel="member",
        )
    )
    assert response["member_price_compliant"] is True


def test_validate_without_member_fields_omits_flag():
    response = validate(PromoIn(sku="SKU-OK", was_price=10.00, now_price=9.00))
    assert "member_price_compliant" not in response
