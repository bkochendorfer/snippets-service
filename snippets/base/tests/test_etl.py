from datetime import date
from unittest.mock import patch

from django.test import TestCase

from snippets.base import etl
from snippets.base.models import DailyImpressions, Job, JobDailyPerformance
from snippets.base.tests import JobFactory


class TestRedashRows(TestCase):
    @patch('snippets.base.etl.redash.query',
           return_value={'query_result': {'data': {'rows': ['mock rows']}}})
    def test_base(self, query):
        d = date(2019, 12, 19)
        query_name, query_id = next(iter(etl.REDASH_QUERY_IDS.items()))
        assert etl.redash_rows(query_name, date=d) == ['mock rows']
        bind_data = {'date': str(d)}
        query.assert_called_with(query_id, bind_data)


class TestUpdateJobMetrics(TestCase):
    def test_base(self):
        JobFactory.create(
            id=1000,
            status=Job.COMPLETED,
            publish_start=date(2020, 1, 1),
            completed_on=date(2020, 1, 10),
        )
        JobFactory.create(id=2000)
        JobDailyPerformance(
            date=date(2020, 1, 9),
            impression=100,
            job=Job.objects.get(id=1000)
        ).save()

        rows = [
            [
                {
                    'message_id': '1000',
                    'event_context': '{}',
                    'event': 'CLICK_BUTTON',
                    'channel': 'release',
                    'country_code': 'GR',
                    'counts': 5,
                    'no_clients': 2,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '1000',
                    'event_context': '{}',
                    'event': 'IMPRESSION',
                    'channel': 'release',
                    'country_code': 'ES',
                    'counts': 30,
                    'no_clients': 10,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '1000',
                    'event_context': '{}',
                    'event': 'IMPRESSION',
                    'channel': 'release',
                    'country_code': 'IT',
                    'counts': 50,
                    'no_clients': 20,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '1000',
                    'event_context': '{}',
                    'event': 'BLOCK',
                    'channel': 'releases',
                    'country_code': 'UK',
                    'counts': 23,
                    'no_clients': 9,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '1000',
                    'event_context': '{}',
                    'event': 'BLOCK',
                    'channel': 'beta-test',
                    'country_code': 'SW',
                    'counts': 27,
                    'no_clients': 50,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '1000',
                    'event_context': 'EOYSnippetForm',
                    'event': 'CLICK_BUTTON',
                    'additional_properties': (
                        '{"source":"NEWTAB_FOOTER_BAR_CONTENT","id":"NEWTAB_FOOTER_BAR_CONTENT"}'
                    ),
                    'channel': 'release',
                    'country_code': 'IT',
                    'counts': 10,
                    'no_clients': 4,
                    'no_clients_total': 0,
                },
                # To be discarded
                {
                    'message_id': '500',
                    'event_context': '{}',
                    'event': 'CLICK',
                    'channel': 'demo',
                    'country_code': 'GR',
                    'counts': 5,
                    'no_clients': 10,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '1000',
                    'event_context': '',
                    'event': 'CLICK',
                    'channel': 'release',
                    'country_code': 'GR',
                    'counts': 6,
                    'no_clients': 10,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '2000',
                    'event_context': '{}',
                    'event': 'CLICK_BUTTON',
                    'additional_properties': '{"value": "scene1-button-learn-more", "foo": "bar"}',
                    'channel': 'release',
                    'country_code': 'GR',
                    'counts': 44,
                    'no_clients': 33,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '2000',
                    'event_context': '{}',
                    'event': 'CLICK_BUTTON',
                    'channel': 'release',
                    'country_code': 'BG',
                    'counts': 3,
                    'no_clients': 10,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '2000',
                    'event_context': '{}',
                    'event': 'CLICK_BUTTON',
                    'channel': 'release',
                    'country_code': 'AL',
                    'counts': 1,
                    'no_clients': 10,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '2000',
                    'event_context': 'conversion-subscribe-activation',
                    'event': 'CLICK_BUTTON',
                    'additional_properties': '{"foo": "bar"}',
                    'channel': 'release',
                    'country_code': 'GR',
                    'counts': 5,
                    'no_clients': 8,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '2000',
                    'event_context': 'subscribe-error',
                    'event': 'CLICK_BUTTON',
                    'additional_properties': '{"foo": "bar"}',
                    'channel': 'release',
                    'country_code': 'GR',
                    'counts': 3,
                    'no_clients': 4,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '2000',
                    'event_context': 'subscribe-success',
                    'event': 'CLICK_BUTTON',
                    'channel': 'release',
                    'country_code': 'ERROR',
                    'counts': 9,
                    'no_clients': 57,
                    'no_clients_total': 0,
                },
                {
                    'message_id': '2000',
                    'event_context': '',
                    'event': 'DISMISS',
                    'channel': 'beta',
                    'country_code': 'ERROR',
                    'counts': 1,
                    'no_clients': 1,
                    'no_clients_total': 0,
                },
            ],
            [
                {
                    'message_id': '1000',
                    'event_context': '',
                    'event': 'IMPRESSION',
                    'channel': 'release',
                    'country_code': 'ES',
                    'counts': 0,
                    'no_clients': 0,
                    'no_clients_total': 232,
                },
                {
                    'message_id': '1000',
                    'event_context': '',
                    'event': 'IMPRESSION',
                    'channel': 'release',
                    'country_code': 'IT',
                    'counts': 0,
                    'no_clients': 0,
                    'no_clients_total': 421,
                },
            ],
        ]

        with patch('snippets.base.etl.redash_rows') as redash_rows_mock:
            redash_rows_mock.side_effect = rows
            result = etl.update_job_metrics(date(2020, 1, 10))

        self.assertEqual(redash_rows_mock.call_count, 2)
        self.assertTrue(result)
        self.assertEqual(JobDailyPerformance.objects.count(), 3)

        jdp1 = JobDailyPerformance.objects.filter(job_id=1000).order_by('-id')[0]
        self.assertEqual(jdp1.impression, 80)
        self.assertEqual(jdp1.impression_no_clients_total, 653)
        self.assertEqual(jdp1.click, 21)
        self.assertEqual(jdp1.block, 50)
        self.assertEqual(jdp1.dismiss, 0)
        self.assertEqual(jdp1.go_to_scene2, 0)
        self.assertEqual(jdp1.subscribe_error, 0)
        self.assertEqual(jdp1.subscribe_success, 0)
        self.assertEqual(jdp1.other_click, 0)
        self.assertEqual(len(jdp1.details), 6)
        for detail in [
                {'event': 'click', 'counts': 11, 'channel': 'release',
                 'country': 'GR', 'no_clients': 12, 'no_clients_total': 0},
                {'event': 'impression', 'counts': 30, 'channel': 'release',
                 'country': 'ES', 'no_clients': 10, 'no_clients_total': 232},
                {'event': 'impression', 'counts': 50, 'channel': 'release',
                 'country': 'IT', 'no_clients': 20, 'no_clients_total': 421},
                {'event': 'block', 'counts': 23, 'channel': 'release',
                 'country': 'UK', 'no_clients': 9, 'no_clients_total': 0},
                {'event': 'block', 'counts': 27, 'channel': 'beta',
                 'country': 'SW', 'no_clients': 50, 'no_clients_total': 0}
        ]:
            self.assertTrue(detail in jdp1.details)

        jdp2 = JobDailyPerformance.objects.get(job_id=2000)
        self.assertEqual(jdp2.impression, 0)
        self.assertEqual(jdp2.impression_no_clients_total, 0)
        self.assertEqual(jdp2.click, 5)
        self.assertEqual(jdp2.block, 0)
        self.assertEqual(jdp2.dismiss, 1)
        self.assertEqual(jdp2.go_to_scene2, 44)
        self.assertEqual(jdp2.subscribe_error, 3)
        self.assertEqual(jdp2.subscribe_success, 9)
        self.assertEqual(jdp2.other_click, 4)
        self.assertEqual(len(jdp2.details), 7)
        for detail in [
                {'event': 'go_to_scene2', 'counts': 44, 'channel': 'release',
                 'country': 'GR', 'no_clients': 33, 'no_clients_total': 0},
                {'event': 'other_click', 'counts': 3, 'channel': 'release',
                 'country': 'BG', 'no_clients': 10, 'no_clients_total': 0},
                {'event': 'other_click', 'counts': 1, 'channel': 'release',
                 'country': 'AL', 'no_clients': 10, 'no_clients_total': 0},
                {'event': 'click', 'counts': 5, 'channel': 'release',
                 'country': 'GR', 'no_clients': 8, 'no_clients_total': 0},
                {'event': 'subscribe_error', 'counts': 3, 'channel': 'release',
                 'country': 'GR', 'no_clients': 4, 'no_clients_total': 0},
                {'event': 'subscribe_success', 'counts': 9, 'channel': 'release',
                 'country': 'XX', 'no_clients': 57, 'no_clients_total': 0},
                {'event': 'dismiss', 'counts': 1, 'channel': 'beta',
                 'country': 'XX', 'no_clients': 1, 'no_clients_total': 0}
        ]:
            self.assertTrue(detail in jdp2.details)


class TestUpdateImpressions(TestCase):
    def test_base(self):
        with patch('snippets.base.etl.redash_rows') as rr_mock:
            rr_mock.side_effect = [
                [
                    {
                        'channel': 'release',
                        'counts': 100,
                        'duration': '4',
                        'no_clients': 40,
                    },
                    {
                        'channel': 'foo',
                        'counts': 33,
                        'duration': '4',
                        'no_clients': 50,
                    },
                    {
                        'channel': 'nightlyz',  # ending `z` on purpose
                        'counts': 10,
                        'duration': '5',
                        'no_clients': 30,
                    },
                    {
                        'channel': 'release',
                        'counts': 2,
                        'duration': '6',
                        'no_clients': 20,
                    },

                ],
            ]
            self.assertEqual(etl.update_impressions('2019-12-20'), 3)
        self.assertEqual(DailyImpressions.objects.all().count(), 1)

        di = DailyImpressions.objects.all()[0]
        self.assertTrue(
            {'channel': 'release', 'duration': '4', 'counts': 133, 'no_clients': 40}
            in di.details
        )
        self.assertTrue(
            {'channel': 'release', 'duration': '6', 'counts': 2, 'no_clients': 20}
            in di.details
        )
        self.assertTrue(
            {'channel': 'nightly', 'duration': '5', 'counts': 10, 'no_clients': 30}
            in di.details
        )
