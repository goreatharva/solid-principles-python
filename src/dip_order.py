
"""D — Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules; both should depend on
abstractions. We define a `PaymentGateway` abstraction and inject it into
`OrderProcessor`. This allows swapping gateways (e.g., Stripe/PayPal/Fake) without
changing the high-level logic.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str) -> str:
        
        ...

class FakeGateway(PaymentGateway):
    def __init__(self, will_succeed: bool = True) -> None:
        self.will_succeed = will_succeed
        self.charges: list[tuple[float, str]] = []

    def charge(self, amount: float, currency: str) -> str:
        if not self.will_succeed:
            raise RuntimeError('Payment failed')
        self.charges.append((amount, currency))
        return f"TXN-{len(self.charges):06d}"

@dataclass
class Order:
    items: list[tuple[str, float]]  # (name, price)

    def total(self) -> float:
        return sum(price for _, price in self.items)

class OrderProcessor:
    def __init__(self, gateway: PaymentGateway) -> None:
        self.gateway = gateway

    def checkout(self, order: Order, currency: str = 'USD') -> str:
        amount = order.total()
        if amount <= 0:
            raise ValueError('Order total must be positive')
        return self.gateway.charge(amount, currency)
