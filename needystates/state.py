from copy import deepcopy
from .need import Need
from .operations import StateOperations


def smart_append(target_list, value):
    """
    Only append value to a list if it is not None
    :param target_list:
        List to be mutated
    :param value:
        Value to conditionally add. If value is a list, values will be appended individually
    """
    if value is not None:
        if isinstance(value, list):
            for li in value:
                target_list.append(li)
        else:
            target_list.append(value)


class State(object):

    attribute_descriptors = {}

    def __init__(self, config_dictionary,
                 parent_states=None,
                 address_path=None,
                 state_name=None,
                 metadata: dict = {},
                 need_template=Need):
        """
        Dict-like data structures are de-seralized into states for comparison
        :param config_dictionary:
            A dictionary to de-seralize into a state
        :param parent_states:
            Used when recursively creating sub-states
        :param state_name:
            Name of the module that created the state
        :param need_template:
            Used to supply a custom need class for custom attribute descriptors
        """
        self.need_template = need_template
        self.config_keys = []
        self.metadata = metadata
        if parent_states and isinstance(parent_states, list):
            self.parent_states = deepcopy(parent_states)
        else:
            self.parent_states = []
        if address_path and isinstance(address_path, list):
            self.address_path = deepcopy(address_path)
        else:
            self.address_path = []
        if state_name is not None:
            self.name = state_name
        else:
            self.name = ''
        sub_module_parent_chain = self.parent_states
        if self.name:
            sub_module_parent_chain.append(self.name)
        for k, v in config_dictionary.items():
            self.config_keys.append(k)
            if isinstance(v, dict):
                setattr(self, k, State(v,
                                       parent_states=sub_module_parent_chain,
                                       state_name=k,
                                       address_path=self.address_path,
                                       metadata=self.metadata),
                        )
            elif isinstance(v, list):
                temp_list = []
                for item in v:
                    if isinstance(item, dict):
                        sub_parent_modules = deepcopy(sub_module_parent_chain)
                        temp_list.append(State(item,
                                               parent_states=sub_parent_modules,
                                               state_name=v.index(item),
                                               address_path=self.address_path,
                                               metadata=self.metadata))
                    else:
                        temp_list.append(item)
                setattr(self, k, temp_list)
            else:
                setattr(self, k, v)

    def render_dict(self):
        """
        This recursively renders the state as a dict
        :return:
            dict Representing the state
        """
        rendered_dict = {}
        for key in self.config_keys:
            value = getattr(self, key)
            if isinstance(value, State):
                rendered_dict.update({key: value.render_dict()})
            elif isinstance(value, list):
                newlist = []
                for li in value:
                    if isinstance(li, State):
                        newlist.append(li.render_dict())
                    else:
                        newlist.append(li)
                rendered_dict.update({key: newlist})
            else:
                rendered_dict.update({key: value})
        return rendered_dict

    def determine_needs(self, other, strict=False):
        """
        Pass another instance of State to this method in order to generate a list of needs.
        :param other:
            An instance of State, or subclassed Instance of State
        :param strict:
            If Strict is True, DELETE states will be created for attributes present in other but not present in self
        :return:
            A list of Need objects representing needed changes between the two states
        """
        needs_list = []
        for attribute in self.config_keys:
            value = getattr(self, attribute)
            if isinstance(value, State):
                smart_append(needs_list, self._determine_needs_substate(attribute,
                                                                        other,
                                                                        strict=strict))
            elif isinstance(value, bool):
                smart_append(needs_list, self._determine_needs_bool(attribute, other))
            elif isinstance(value, int) or isinstance(value, str):
                smart_append(needs_list, self._determine_needs_int_or_str(attribute, other))
        if strict:
            for attribute in other.config_keys:
                if getattr(self, attribute, None) is None:
                    old_value = getattr(other, attribute)
                    smart_append(needs_list, self.create_need(
                        attribute,
                        StateOperations.DELETE,
                        address_path=self.address_path,
                        parent_states=self.parent_states,
                        old_value=old_value,
                        metadata=self.metadata
                    ))
        return needs_list

    def _determine_needs_bool(self, attribute, other):
        our_value = getattr(self, attribute, None)
        other_value = getattr(other, attribute, None)
        if our_value != other_value:
            return self.create_need(
                attribute,
                StateOperations.SET,
                address_path=self.address_path,
                parent_states=self.parent_states,
                value=our_value,
                old_value=other_value,
                metadata=self.metadata
            )

    def _determine_needs_int_or_str(self, attribute, other):
        """
        Called by determine needs when it encounters an int or str
        :param attribute:
            Name of the attribute being compared
        :param other:
            The other State class being compared
        :return:
            Need object is returned if the states differ
        """
        our_value = getattr(self, attribute, None)
        other_value = getattr(other, attribute, None)
        if our_value:
            if not other_value or our_value != other_value:
                return self.create_need(
                    attribute,
                    StateOperations.SET,
                    address_path=self.address_path,
                    parent_states=self.parent_states,
                    value=our_value,
                    old_value=other_value,
                    metadata=self.metadata
                )

    def create_need(self,
                    attribute,
                    state_operation,
                    address_path=None,
                    parent_states=None,
                    value=None,
                    old_value=None,
                    metadata={}):
        params_dict = {}
        if address_path:
            params_dict.update({'address_path': address_path})
        if parent_states:
            params_dict.update({'parent_states': parent_states})
        # Take heed, False is a legitimate value
        if value or value is False:
            params_dict.update({'value': value})
        if old_value or old_value is False:
            params_dict.update({'old_value': old_value})
        if metadata:
            params_dict.update({'metadata': metadata})
        for key, value in self.attribute_descriptors.items():
            if key == attribute:
                for sk, sv in value.items():
                    if sk == state_operation:
                        params_dict.update({'description': sv})
        return self.need_template(attribute, state_operation, **params_dict)

    def _determine_needs_substate(self, attribute, other, strict=False):
        """
        Called by determine_needs to initiate tail recursion
        :param attribute:
            attribute of the sub_state
        :param other:
            The other parent state
        :param strict:
            If strict is True, DELETE operations will be created
        :return:
        """
        our_value = getattr(self, attribute, None)
        other_value = getattr(other, attribute, None)
        if other_value is None:
            other_value = State({}, metadata = self.metadata)
        return our_value.determine_needs(other_value, strict=strict)

    def __eq__(self, other):
        """
        This ensures that comparisons between state instances only consider keys
        :param other:
            The module we are comparing to
        :return:
            True or False
        """
        return all(getattr(self, key) == getattr(other, key) for key in self.config_keys)
