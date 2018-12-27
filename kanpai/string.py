from .validator import Validator


class String(Validator):

    def __assert_string(self, data, attribs):
        if data is None:
            return self.validation_success(data)

        data_type = type(data)
        if data_type is int or data_type is float or data_type is str:
            return self.validation_success(str(data))
        else:
            return self.validation_error(data, attribs['error'])

    def __init__(self, error='Value must be a string'):
        self.processors = []
        self.processors.append({
            'action': self.__assert_string,
            'attribs': {
                'error': error
            }
        })

    def __assert_required(self, data, attribs):
        if data is None or len(data) is 0:
            return self.validation_error(data, attribs['error'])
        else:
            return self.validation_success(data)

    def required(self, error='Value is required'):
        self.processors.append({
            'action': self.__assert_required,
            'attribs': {
                'error': error
            }
        })
        return self

    def __assert_max(self, data, attribs):
        if data is not None and len(data) > attribs['max_length']:
            return self.validation_error(data, attribs['error'])
        else:
            return self.validation_success(data)

    def max(self, max_length, error=None):
        if max_length is None or type(max_length) is not int:
            raise ValueError(
                'value for max_length is expected to be an integer')

        if error is None:
            self.processors.append({
                'action': self.__assert_max,
                'attribs': {
                    'max_length': max_length,
                    'error': f"Maximum length allowed is {max_length}"
                }
            })
        else:
            self.processors.append({
                'action': self.__assert_max,
                'attribs': {
                    'max_length': max_length,
                    'error': error
                }
            })

        return self

    def __trim(self, data, attribs):
        return self.validation_success(data.strip() if data is not None else None)

    def trim(self):
        self.processors.append({
            'action': self.__trim,
            'attribs': None
        })
        return self