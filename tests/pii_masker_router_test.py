# -*- coding: utf-8 -*-
import pytest

from app.routes.pii_masker.pii_masker_router import (MaskType, PIIType,
                                                     process_pii)


def test_process_pii_mask():
    text = "My name is John Doe and my email is john.doe@example.com"
    mask_type = MaskType.MASK
    pii_types = [PIIType.NAME, PIIType.EMAIL]
    expected_result = "My name is <NAME> and my email is <EMAIL>"

    result = process_pii(text, mask_type, pii_types)

    assert result == expected_result


def test_process_pii_encrypt():
    text = "My credit card number is 1234-5678-9012-3456"
    mask_type = MaskType.ENCRYPT
    pii_types = [PIIType.CREDIT_CARD]
    encryption_key = "IFcBsIUURnIxCweQ7RItuMmG5DSc_sbTHD71bZ5xBQA="

    result = process_pii(text, mask_type, pii_types)
    assert result != text
    assert result != ""
    assert result != "I want you to know all my data! My credit card is 374245455400126"


def test_process_pii_decrypt():
    text = "I want you to know all my data! My credit card is gAAAAABmoOn7dAk73t0Fy11bZwhLUPOQ8EVKjv-zLo5paWSk4mv8EKI3XrGd1iIJMPg-XgicZ9b5AAQh81Pc1XrBHZfORQMS8w=="
    mask_type = MaskType.DECRYPT
    pii_types = [PIIType.CREDIT_CARD]
    encryption_key = "IFcBsIUURnIxCweQ7RItuMmG5DSc_sbTHD71bZ5xBQA="

    result = process_pii(text, mask_type, pii_types, encryption_key=encryption_key)

    assert result != text
    assert result != ""
    assert (
        result
        != "My encrypted credit card number is gAAAAABmoOn7dAk73t0Fy11bZwhLUPOQ8EVKjv-zLo5paWSk4mv8EKI3XrGd1iIJMPg-XgicZ9b5AAQh81Pc1XrBHZfORQMS8w=="
    )


def test_process_pii_detect():
    text = "My name is John Doe and my email is john.doe@example.com"
    mask_type = MaskType.DETECT
    pii_types = [PIIType.NAME, PIIType.EMAIL]

    result = process_pii(text, mask_type, pii_types)

    assert result == "PII_DATA FOUND IN INPUT"


def test_process_pii_invalid_encryption_key():
    text = "My credit card number is 1234-5678-9012-3456"
    mask_type = MaskType.ENCRYPT
    pii_types = [PIIType.CREDIT_CARD]
    encryption_key = "invalid-key"

    with pytest.raises(ValueError):
        process_pii(text, mask_type, pii_types, encryption_key=encryption_key)
