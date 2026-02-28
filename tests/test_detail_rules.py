import unittest

from pipelines.key_point_details.service import details_for_point


class DetailRuleTests(unittest.TestCase):
    def test_known_sort_rule_returns_details(self) -> None:
        details = details_for_point(
            "lists",
            "Use list.sort() when you want in-place ordering; sorted returns a new list.",
        )
        self.assertTrue(details)

    def test_known_scope_rule_returns_details(self) -> None:
        details = details_for_point(
            "scope",
            "Without global, this can cause UnboundLocalError when rebinding names.",
        )
        self.assertTrue(details)

    def test_detail_shape_is_consistent(self) -> None:
        details = details_for_point(
            "booleans",
            "`is` checks identity while `==` checks value equivalence.",
        )
        self.assertTrue(details)
        for detail in details:
            self.assertIn("kind", detail)
            self.assertIn("title", detail)
            has_body = bool(detail.get("text")) or bool(detail.get("code")) or bool(detail.get("table"))
            self.assertTrue(has_body, f"Detail has no body: {detail}")


if __name__ == "__main__":
    unittest.main()
