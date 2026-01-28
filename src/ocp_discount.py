
"""O — Open/Closed Principle (OCP)

Open for extension, closed for modification.
We define a `DiscountStrategy` interface and a `PriceCalculator` that accepts
any strategy. Adding a new discount should not require changing `PriceCalculator`.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float: ...

@dataclass
class PercentageDiscount(DiscountStrategy):
    percent: float  # e.g., 10 for 10%

    def apply(self, price: float) -> float:
        return max(0.0, price * (1 - self.percent / 100))

@dataclass
class FlatDiscount(DiscountStrategy):
    amount: float

    def apply(self, price: float) -> float:
        return max(0.0, price - self.amount)

class PriceCalculator:
    def __init__(self, strategy: DiscountStrategy) -> None:
        self._strategy = strategy

    def total(self, price: float) -> float:
        return self._strategy.apply(price)
