from decimal import Decimal
import pytest
from agent.policies.spending import SpendingManager, SpendingPolicy

def test_payment_within_limit():
    manager = SpendingManager(SpendingPolicy(Decimal("0.01"), Decimal("0.10")))
    manager.authorize(Decimal("0.001"))
    assert manager.spent_usd == Decimal("0.001")

def test_payment_over_single_limit():
    manager = SpendingManager(SpendingPolicy(Decimal("0.01"), Decimal("0.10")))
    with pytest.raises(ValueError):
        manager.authorize(Decimal("0.02"))

def test_session_limit():
    manager = SpendingManager(SpendingPolicy(Decimal("0.01"), Decimal("0.01")))
    manager.authorize(Decimal("0.01"))
    with pytest.raises(ValueError):
        manager.authorize(Decimal("0.001"))
