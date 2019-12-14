from copy import deepcopy
from .need import Need
from .operations import StateOperations

class State(object):

    def __init__(self, config_dictionary, parent_states=None, address_path=None, state_name=None):
        """
        Dict-like data structures are de-seralized into states for comparison
        :param config_dictionary:
            A dictionary to de-seralize into a state
        :param parent_states:
            Used when recursively creating sub-states
        :param state_name:
            Name of the module that created the state
        """
        self.config_keys = []
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
        sub_module_parent_chain.append(self.name)
        for k, v in config_dictionary.items():
            self.config_keys.append(k)
            if isinstance(v, dict):
                setattr(self, k, State(v, parent_states=sub_module_parent_chain, state_name=k))
            elif isinstance(v, list):
                temp_list = []
                for item in v:
                    if isinstance(item, dict):
                        sub_parent_modules = deepcopy(sub_module_parent_chain)
                        temp_list.append(State(item, parent_states=sub_parent_modules, state_name=v.index(item)))
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
        needs_list = []
        for attribute in self.config_keys:
            value = getattr(self, attribute)
            if isinstance(value, State):
                needs_list = needs_list + self._determine_needs_substate(attribute,
                                                                         other,
                                                                         strict=strict)
            elif isinstance(value, int) or isinstance(value, str):
                needs_list.append(self._determine_needs_int_or_str(attribute, other))
        return needs_list

    def _determine_needs_int_or_str(self, attribute, other):
        our_value = getattr(self, attribute, None)
        other_value = getattr(other, attribute, None)
        if our_value:
            if not other_value or our_value != other_value:
                return Need(
                    attribute,
                    StateOperations.SET,
                    address_path=self.address_path,
                    parent_states=self.parent_states,
                    value=our_value,
                    old_value=other_value
                )

    def _determine_needs_substate(self, attribute, other, strict=False):
        our_value = getattr(self, attribute, None)
        other_value = getattr(other, attribute, None)
        if other_value is None:
            other_value = State({})
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
