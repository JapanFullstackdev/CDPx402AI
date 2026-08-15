from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from threading import Lock

@dataclass(frozen=True)
class SpendingPolicy:
    max_single_payment_usd: Decimal = Decimal("0.01")
    max_session_spend_usd: Decimal = Decimal("0.10")

class SpendingManager:
    def __init__(self, policy: SpendingPolicy | None = None) -> None:
        self.policy = policy or SpendingPolicy()
        self._spent_usd = Decimal("0")
        self._lock = Lock()

    @property
    def spent_usd(self) -> Decimal:
        with self._lock:
            return self._spent_usd

    @property
    def remaining_usd(self) -> Decimal:
        with self._lock:
            return self.policy.max_session_spend_usd - self._spent_usd

    def authorize(self, amount_usd: Decimal) -> None:
        amount = Decimal(str(amount_usd))
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        if amount > self.policy.max_single_payment_usd:
            raise ValueError(f"Payment rejected: ${amount} exceeds single-payment limit ${self.policy.max_single_payment_usd}.")
        with self._lock:
            total = self._spent_usd + amount
            if total > self.policy.max_session_spend_usd:
                raise ValueError(f"Payment rejected: session limit would be exceeded. current=${self._spent_usd}, requested=${amount}, limit=${self.policy.max_session_spend_usd}.")
            self._spent_usd = total

    def reset(self) -> None:
        with self._lock:
            self._spent_usd = Decimal("0")

spending_manager = SpendingManager()
