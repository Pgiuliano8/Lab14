from dataclasses import dataclass

from model.orders import Order


@dataclass
class Arco:
    o1: Order
    o2: Order
    peso: int