from fazaconta_backend.shared.domain.exceptions.DomainException import DomainException


class BusinessRuleValidationException(DomainException):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)
