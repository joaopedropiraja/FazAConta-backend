from .exceptions import BusinessRuleValidationException
from .business_rule import BusinessRule


class BusinessRuleValidationMixin:
    def check_rule(self, rule: BusinessRule):
        if rule.is_broken():
            raise BusinessRuleValidationException(rule)
