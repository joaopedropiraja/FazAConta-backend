from dataclasses import dataclass
from .business_rule import BusinessRule


class DomainException(Exception): ...


class BusinessRuleValidationException(DomainException):
    rule: BusinessRule

    def __str__(self):
        return str(self.rule)
