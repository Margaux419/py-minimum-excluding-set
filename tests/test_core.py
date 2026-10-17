import unittest

from py_minimum_excluding_set import MinimumExcludingSet


class TestEmpty(unittest.TestCase):
    def test_empty_starts_at_zero(self):
        s = MinimumExcludingSet()
        self.assertEqual(s.value(), 0)
        self.assertEqual(len(s), 0)

    def test_repr_shows_value(self):
        s = MinimumExcludingSet()
        self.assertEqual(repr(s), "MinimumExcludingSet(value=0, size=0)")


class TestAdd(unittest.TestCase):
    def test_add_zero_advances_to_one(self):
        s = MinimumExcludingSet()
        s.add(0)
        self.assertEqual(s.value(), 1)

    def test_add_gap_keeps_zero(self):
        s = MinimumExcludingSet()
        s.add(5)
        self.assertEqual(s.value(), 0)

    def test_fill_gap_in_order(self):
        s = MinimumExcludingSet()
        for i in range(5):
            s.add(i)
        self.assertEqual(s.value(), 5)

    def test_fill_gap_out_of_order(self):
        s = MinimumExcludingSet()
        for i in (2, 0, 4, 1, 3):
            s.add(i)
        self.assertEqual(s.value(), 5)

    def test_duplicate_add_is_noop(self):
        s = MinimumExcludingSet()
        s.add(0)
        s.add(0)
        self.assertEqual(len(s), 1)
        self.assertEqual(s.value(), 1)

    def test_negative_rejected(self):
        s = MinimumExcludingSet()
        with self.assertRaises(ValueError):
            s.add(-1)


class TestContains(unittest.TestCase):
    def test_contains_after_add(self):
        s = MinimumExcludingSet()
        s.add(3)
        self.assertIn(3, s)
        self.assertNotIn(2, s)


class TestDiscard(unittest.TestCase):
    def test_discard_present(self):
        s = MinimumExcludingSet()
        s.add(0)
        s.discard(0)
        self.assertNotIn(0, s)
        # MEX returns to 0
        self.assertEqual(s.value(), 0)

    def test_discard_above_mex(self):
        s = MinimumExcludingSet()
        for i in range(3):
            s.add(i)
        s.discard(5)
        self.assertEqual(s.value(), 3)

    def test_discard_missing_value(self):
        s = MinimumExcludingSet()
        s.add(0)
        s.discard(0)
        s.discard(0)
        self.assertEqual(s.value(), 0)
        self.assertEqual(len(s), 0)


class TestInterleaved(unittest.TestCase):
    def test_add_discard_add(self):
        s = MinimumExcludingSet()
        s.add(0)
        self.assertEqual(s.value(), 1)
        s.discard(0)
        self.assertEqual(s.value(), 0)
        s.add(0)
        self.assertEqual(s.value(), 1)

    def test_stale_candidates_after_adds(self):
        s = MinimumExcludingSet()
        s.add(5)
        s.add(0)
        s.add(1)
        s.add(2)
        self.assertEqual(s.value(), 3)

    def test_query_idempotent(self):
        s = MinimumExcludingSet()
        s.add(5)
        s.add(3)
        self.assertEqual(s.value(), 0)
        self.assertEqual(s.value(), 0)

    def test_large_sparse(self):
        s = MinimumExcludingSet()
        for i in (1000, 100, 10):
            s.add(i)
        self.assertEqual(s.value(), 0)
        s.add(0)
        self.assertEqual(s.value(), 1)


if __name__ == "__main__":
    unittest.main()
