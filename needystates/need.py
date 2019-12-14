class Need(object):

    def __init__(self,
                 attribute,
                 operation,
                 address_path=None,
                 parent_states=None,
                 value=None,
                 old_value=None,
                 description=''):
        """
        Needs are generated to describe the path to get from one configuration to another.

        :param attribute:
            The attribute of the state or module on which the operation is to be performed

        :param operation:
            The Operation to be performed

        :param address_path:
            Arbitrarily address path to differentiate states intended to be executed by different providers

        :param parent_states:
            Used when creating needs to be performed by sub_states

        :param value:
            For use with Operations that require a value

        :param old_value:
            (Optional) When rendering the need as text, the old value can be displayed to provide more context for the
            user

        :param description:
            (Optional) Provide a more detailed description for the need
        """
        self.attribute = attribute
        self.operation = operation
        if address_path and isinstance(address_path, list):
            self.address_path = address_path
        else:
            self.address_path = []
        if parent_states and isinstance(parent_states, list):
            self.parent_states = parent_states
        else:
            self.parent_states = []

        self.value = value
        self.old_value = old_value
        self.description = description

    def get_short_string(self):
        """
        :return:
              A string suitibile to display to the user, detailed enough for them to grasp the intent of the need
            Example:
                dbconfmodule.dbConfigManager|server.url:SET=https://example.com
        """
        if self.address_path:
            address_path = '.'.join(self.address_path)
            address_path = f"{address_path}|"
        else:
            address_path = ''
        if self.parent_states:
            parent_states = '.'.join(self.parent_states)
            parent_states = f"{parent_states}."
        else:
            parent_states = ''
        if self.value:
            value = f"={self.value}"
        else:
            value = ''
        return f"{address_path}{parent_states}{self.attribute}.{self.operation.name}{value}"

    def get_long_string(self):
        """
        :return:
            A body of simply formatted text to describe in depth what action is to be performed
        """
        return f"{self.get_short_string()}\n----------\n{self.description}"

    def __eq__(self, other):
        return all(getattr(self, key) == getattr(other, key) for key in ['attribute',
                                                                         'operation',
                                                                         'address_path',
                                                                         'parent_states',
                                                                         'value',
                                                                         'old_value',
                                                                         'description'])
