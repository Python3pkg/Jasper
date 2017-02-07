from jasper import Scenario, given, when, then, Expect, Context
from unittest import TestCase
import asyncio

class TestFeatureArithmetic(TestCase):

    def setUp(self):
        @given
        def an_adding_function(context):
            context.function = lambda a, b: a + b
            context.called_given = True

        @given
        def a_multiplication_function(context):
            context.function = lambda a, b: a * b
            context.called_given = True

        @when
        def we_call_it_with_two_negative_numbers(context):
            return {
                'called_when': True,
                'return_val': context.function(-5, -5)
            }

        @when
        def we_call_it_with_two_positive_numbers(context):
            return {
                'called_when': True,
                'return_val': context.function(5, 5)
            }

        @then
        def we_will_get_a_negative_number(context):
            context.result['called_then'] = True
            Expect(context.result['return_val']).to_be.less_than(0)

        @then
        def we_will_get_a_positive_number(context):
            context.result['called_then'] = True
            Expect(context.result['return_val']).to_be.greater_than(0)

        self.scenarios = [
            Scenario(
                'Adding two negative numbers',
                given=an_adding_function,
                when=we_call_it_with_two_negative_numbers,
                then=we_will_get_a_negative_number
            ),
            Scenario(
                'Adding two positive numbers',
                given=an_adding_function,
                when=we_call_it_with_two_positive_numbers,
                then=we_will_get_a_positive_number
            ),
            Scenario(
                'Multiplying two negative numbers',
                given=a_multiplication_function,
                when=we_call_it_with_two_negative_numbers,
                then=we_will_get_a_positive_number
            ),
            Scenario(
                'Multiplying two positive numbers',
                given=a_multiplication_function,
                when=we_call_it_with_two_positive_numbers,
                then=we_will_get_a_positive_number
            )
        ]

    def test_run(self):
        loop = asyncio.get_event_loop()
        for scenario in self.scenarios:
            self.assertFalse(scenario.passed)

            scenario.context = Context()
            loop.run_until_complete(scenario.run())

            self.assertTrue(scenario.context.called_given)
            self.assertTrue(scenario.context.result['called_when'])
            self.assertTrue(scenario.context.result['called_then'])

            self.assertTrue(scenario.passed)
