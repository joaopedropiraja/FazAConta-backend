from BusinessRule import BusinessRule
from exceptions.BusinessRuleValidationException import BusinessRuleValidationException


class BusinessRuleValidationMixin:
    def check_rule(self, rule: BusinessRule):
        if rule.is_broken():
            raise BusinessRuleValidationException(rule)
