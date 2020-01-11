from unittest import TestCase
from needystates import State, Need, StateOperations

configuration1 = {
    'attribute1': 1,
    'attribute2': 'hello'
}

configuration2 = {
    'attribute1': 1,
    'sub_module': {
        'sub_attr1': 'test'
    }
}

configuration3 = {
    'sub_module_list': [
        {'attribute1': 'test'},
        {'attribute1': 'notest'}
    ],
    'attribute_list': [
        'attr1',
        'attr2'
    ]
}


class TestStateAttributes(TestCase):

    def test_attributes(self):
        state = State(configuration1, state_name='state')
        self.assertEqual(1, state.attribute1)
        self.assertEqual('hello', state.attribute2)

    def test_submodule(self):
        state = State(configuration2, state_name='state')
        sub_state = State(configuration2['sub_module'],
                          state_name='sub_module',
                          parent_states=['state'])
        self.assertEqual(sub_state, state.sub_module)

    def test_submodule_list(self):
        state = State(configuration3, state_name='state')
        sub_state_list_item_1 = State(configuration3['sub_module_list'][0], state_name=0, parent_states=['state'])
        self.assertEqual(sub_state_list_item_1, state.sub_module_list[0])
        self.assertEqual(['attr1', 'attr2'], state.attribute_list)


class TestStateRendering(TestCase):

    def test_deseralize_config1(self):
        state = State(configuration1, state_name='state')
        self.assertEqual(configuration1, state.render_dict())

    def test_deseralize_config2(self):
        state = State(configuration2, state_name='state')
        self.assertEqual(configuration2, state.render_dict())

    def test_deseralize_config3(self):
        state = State(configuration3, state_name='state')
        self.assertEqual(configuration3, state.render_dict())


class TestStateNeedGeneration(TestCase):

    def test_false_value_need_generation(self):
        state1 = State({'attribute': False}, state_name='statetest', address_path=['module1'])
        state2 = State({'attribute': True}, state_name='statetest', address_path=['module1'])
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value=False,
                        old_value=True,
                        parent_states=['statetest'],
                        address_path=['module1'])
        self.assertEqual(expected, result[0])

    def test_need_address_path_generation(self):
        state1 = State({'attribute': 'first_state'}, state_name='statetest', address_path=['module1'])
        state2 = State({'attribute': 'second_state'}, state_name='statetest', address_path=['module1'])
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value='first_state',
                        old_value='second_state',
                        parent_states=['statetest'],
                        address_path=['module1'])
        self.assertEqual(expected, result[0])

    def test_need_noname_generation(self):
        state1 = State({'attribute': 'first_state'})
        state2 = State({'attribute': 'second_state'})
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value='first_state',
                        old_value='second_state'
                        )
        self.assertEqual(expected, result[0])

    def test_need_basic_generation_str(self):
        state1 = State({'attribute': 'first_state'}, state_name='statetest')
        state2 = State({'attribute': 'second_state'}, state_name='statetest')
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value='first_state',
                        old_value='second_state',
                        parent_states=['statetest'])
        self.assertEqual(expected, result[0])

    def test_need_basic_generation_str_with_metadata(self):
        state1 = State({'attribute': 'first_state'}, state_name='statetest', metadata={'attr': 'key'})
        state2 = State({'attribute': 'second_state'}, state_name='statetest')
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value='first_state',
                        old_value='second_state',
                        parent_states=['statetest'],
                        metadata={'attr': 'key'})
        self.assertEqual(expected, result[0])

    def test_need_generation_absent_cstate(self):
        state1 = State({'attribute': 'first_state'}, state_name='statetest')
        state2 = State({}, state_name='statetest')
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value='first_state',
                        parent_states=['statetest'])
        self.assertEqual(expected, result[0])

    def test_need_generation_absent_substate(self):
        state1 = State({'substate': {'attribute': 'first_state'}}, state_name='statetest')
        state2 = State({}, state_name='statetest')
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value='first_state',
                        parent_states=['statetest', 'substate'])
        self.assertEqual(expected, result[0])

    def test_nested_need_generation_str(self):
        state1 = State({'sub_state': {'attribute': 'newval'}}, state_name='statetest')
        state2 = State({'irrelevant_attribute': False, 'sub_state': {'attribute': 'oldval'}}, state_name='statetest')
        result = state1.determine_needs(state2)
        expected = Need('attribute',
                        StateOperations.SET,
                        value='newval',
                        old_value='oldval',
                        parent_states=['statetest', 'sub_state'],
                        )
        self.assertEqual(expected, result[0])

    def test_strict_need_generation(self):
        state1 = State({}, state_name='statetest')
        state2 = State({'deleteme': False}, state_name='statetest')
        result = state1.determine_needs(state2, strict=True)
        expected = Need('deleteme',
                        StateOperations.DELETE,
                        old_value=False,
                        parent_states=['statetest'],
                        )
        self.assertEqual(expected, result[0])

    def test_attribute_descriptor_selection(self):
        class TestState(State):
            attribute_descriptors = {
                'test': {
                    StateOperations.SET: 'This is a custom descriptor'
                }
            }
        state1 = TestState({'test': True}, state_name='teststate')
        state2 = TestState({'test': False}, state_name='teststate')
        needs = state1.determine_needs(state2)
        result = needs[0].get_long_string()
        self.assertEqual('teststate.test.SET=True\n----------\nThis is a custom descriptor', result)