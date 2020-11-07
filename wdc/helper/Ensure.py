from typing import Any, Callable


class Ensure(object):
    def __init__(self, subject: Any):
        self._subject = subject

    def not_none(self, error_message: str = '') -> 'Ensure':
        if self._subject:
            return self
        else:
            raise ValueError(error_message)

    def that_is(self, predicate: Callable[[Any], bool], error_message: str = ''):
        if predicate(self._subject):
            return self
        else:
            raise ValueError(error_message)

    def instance_of(self, expected_type: type, error_message: str = ''):
        if isinstance(self._subject, expected_type):
            return self
        else:
            error_message = \
                f'Should be {expected_type} but was {type(self._subject)}' if error_message == '' else error_message
            raise ValueError(error_message)

    def is_optional_instance_of(self, expected_type: type, error_message: str = ''):
        if not self._subject:
            return self
        elif isinstance(self._subject, expected_type):
            return self
        else:
            raise ValueError(error_message)
