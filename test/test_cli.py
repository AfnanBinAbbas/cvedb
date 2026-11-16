from unittest import TestCase
from unittest.mock import patch

from cvedb.cli import main


class TestUpdateFlag(TestCase):
    def setUp(self):
        p1 = patch("cvedb.cli.CVEdb")
        p2 = patch("cvedb.cli.print_cves")
        self.mock_db_cls = p1.start()
        self.mock_print = p2.start()
        self.addCleanup(p1.stop)
        self.addCleanup(p2.stop)
        self.db = self.mock_db_cls.open.return_value.__enter__.return_value
        self.db.feeds = []

    def test_update_alone_does_not_query(self):
        rc = main(["cvedb", "--update"])
        self.assertEqual(rc, 0)
        self.db.reload.assert_called_once_with(force=True)
        self.mock_print.assert_not_called()

    def test_update_with_query_flag_still_queries(self):
        rc = main(["cvedb", "--update", "--after", "2024-01-01"])
        self.assertEqual(rc, 0)
        self.db.reload.assert_called_once_with(force=True)
        self.mock_print.assert_called_once()

    def test_update_with_search_term_still_queries(self):
        rc = main(["cvedb", "--update", "log4j"])
        self.assertEqual(rc, 0)
        self.db.reload.assert_called_once_with(force=True)
        self.mock_print.assert_called_once()

    def test_update_with_data_version_does_not_print_all_cves(self):
        rc = main(["cvedb", "--update", "--data-version"])
        self.assertEqual(rc, 0)
        self.db.reload.assert_called_once_with(force=True)
        self.mock_print.assert_not_called()

    def test_plain_invocation_still_prints_all(self):
        rc = main(["cvedb"])
        self.assertEqual(rc, 0)
        self.db.reload.assert_not_called()
        self.mock_print.assert_called_once()
