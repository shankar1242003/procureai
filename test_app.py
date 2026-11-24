
import pytest

from agent import (
    calculate_purchase_total,
    check_approval
)

from llm import TicketResult


def test_purchase_total():

    result = calculate_purchase_total.invoke({
        "price": 40000,
        "quantity": 20
    })

    assert result == 800000


def test_approval_required():

    result = check_approval.invoke({
        "amount": 80000
    })

    assert result == (
        "Manager approval is required."
    )


def test_approval_boundary():

    result = check_approval.invoke({
        "amount": 50000
    })

    assert result == (
        "Manager approval is not required."
    )


def test_invalid_quantity():

    with pytest.raises(ValueError):

        calculate_purchase_total.invoke({
            "price": 100,
            "quantity": -5
        })


def test_structured_output():

    result = TicketResult(
        category="Invoice",
        priority="Medium",
        summary="Incorrect invoice",
        suggested_action="Contact finance"
    )

    assert result.category == "Invoice"
