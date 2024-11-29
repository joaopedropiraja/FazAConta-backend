from fazaconta_backend.shared.domain.BusinessRule import BusinessRule
from fazaconta_backend.shared.domain.exceptions.BusinessRuleValidationException import (
    BusinessRuleValidationException,
)


class BusinessRuleValidationMixin:
    def check_rule(self, rule: BusinessRule):
        if rule.is_broken():
            raise BusinessRuleValidationException(rule)
