""" Tests for DomainEvents """
import unittest

from esframework.exceptions import DomainEventException
from esframework.tests.assets import EventA


class TestDomainEvent(unittest.TestCase):
    """ Testing class for Domain Events """

    def test_it_cannot_set_event_id_twice(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198BE", "foo")
        domain_event.set_event_id("6C28E7B7-61A1-432D-8778-DA94BE334969")
        with self.assertRaises(DomainEventException) as ex:
            domain_event.set_event_id("4AFA7DC7-5268-4BE9-B065-27D19CE4DD5F")
        self.assertEqual(str(ex.exception), "Event id can only be set once!")

    def test_it_cannot_set_version_twice(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198BE", "foo")
        domain_event.set_version(1)
        with self.assertRaises(DomainEventException) as ex:
            domain_event.set_version(1)
        self.assertEqual(str(ex.exception), "Version can only be set once!")

    def test_it_cannot_set_correlation_id_twice(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198BE", "foo")
        domain_event.set_correlation_id("6C28E7B7-61A1-432D-8778-DA94BE334969")
        with self.assertRaises(DomainEventException) as ex:
            domain_event.set_correlation_id("4AFA7DC7-5268-4BE9-B065-27D19CE4DD5F")
        self.assertEqual(str(ex.exception), "Correlation id can only be set once!")

    def test_it_cannot_set_causation_id_twice(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198BE", "foo")
        domain_event.set_causation_id("6C28E7B7-61A1-432D-8778-DA94BE334969")
        with self.assertRaises(DomainEventException) as ex:
            domain_event.set_causation_id("4AFA7DC7-5268-4BE9-B065-27D19CE4DD5F")
        self.assertEqual(str(ex.exception), "Causation id can only be set once!")

    def test_it_can_serialize(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198BE", "foo")
        expected_result = {
            'aggregate_root_id': '0A919B3E-5BCB-41DC-B157-8A9E2A7198BE',
            'an_event_property': 'foo',
        }

        self.assertEqual(domain_event.serialize(), expected_result)

    def test_it_can_deserialize(self):
        serialized_data = {
            'aggregate_root_id': '0A919B3E-5BCB-41DC-B157-8A9E2A7198BE',
            'an_event_property': 'foo',
        }

        # domain_event: EventA
        domain_event = EventA.deserialize(serialized_data)
        self.assertEqual(
            domain_event.get_aggregate_root_id(),
            '0A919B3E-5BCB-41DC-B157-8A9E2A7198BE'
        )

        self.assertEqual(
            domain_event.get_an_event_property(),
            'foo'
        )

    def test_it_can_add_metadata(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198BE", "foo")
        domain_event.add_metadata("foo", "__an_event_property")
        self.assertEqual(domain_event.get_metadata(), [{"foo": "__an_event_property"}])

    def test_it_cannot_have_duplicate_metadata(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198B", "foo")
        domain_event.add_metadata("foo", "__an_event_property")
        with self.assertRaises(DomainEventException) as ex:
            domain_event.add_metadata("foo", "__an_event_property")
        self.assertEqual(str(ex.exception), 'Metadata is already set!')

    def test_it_can_remove_metadata(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198BE", "foo")
        domain_event.add_metadata("foo", "__an_event_property")
        self.assertEqual(domain_event.get_metadata(), [{"foo": "__an_event_property"}])
        domain_event.remove_metadata("foo", "__an_event_property")
        self.assertEqual(domain_event.get_metadata(), [])

    def test_it_cannot_remove_not_existent_data(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198B", "foo")
        with self.assertRaises(DomainEventException) as ex:
            domain_event.remove_metadata("foo", "__an_event_property")
        self.assertEqual(str(ex.exception), "Can't remove non existent metadata!")

    def test_it_cant_set_metadata_on_non_existing_properties(self):
        domain_event = EventA("0A919B3E-5BCB-41DC-B157-8A9E2A7198B", "foo")
        with self.assertRaises(DomainEventException) as ex:
            domain_event.add_metadata("foo", "non_existing_prop")
        self.assertEqual(
            str(ex.exception), "Can't set metadata on non existing event properties")
