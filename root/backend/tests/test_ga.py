import asyncio
import os
import sys
import unittest

# Ensure backend package imports resolve when tests run from project root.
BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

import main
from app.services.spacing import GeneticSyllabusOptimizer


class TestGeneticSyllabusOptimizer(unittest.TestCase):
    def test_solve_returns_schedule_with_expected_days(self):
        optimizer = GeneticSyllabusOptimizer(population_size=20, mutation_rate=0.2)
        topics = [
            {"id": "t1", "name": "Linear Algebra", "weight": 3},
            {"id": "t2", "name": "Calculus", "weight": 2},
            {"id": "t3", "name": "Python", "weight": 2},
        ]

        schedule = optimizer.solve(topics, days=5, velocity="Medium")

        self.assertIsInstance(schedule, list)
        self.assertEqual(len(schedule), 5)
        self.assertTrue(all(isinstance(day, list) for day in schedule))

        assigned_ids = {topic["id"] for day in schedule for topic in day}
        self.assertTrue({"t1", "t2", "t3"}.issubset(assigned_ids))

    def test_solve_handles_empty_topics(self):
        optimizer = GeneticSyllabusOptimizer(population_size=10, mutation_rate=0.1)
        schedule = optimizer.solve([], days=3, velocity="Slow")

        self.assertEqual(len(schedule), 3)
        self.assertEqual(sum(len(day) for day in schedule), 0)


class TestMainEndpoints(unittest.TestCase):
    def test_optimize_roadmap_returns_metadata_and_roadmap(self):
        payload = main.OptimizationRequest(
            topics=[
                main.TopicItem(id="t1", name="Math", weight=2),
                main.TopicItem(id="t2", name="Physics", weight=3),
            ],
            days=4,
            velocity="Medium",
        )

        result = asyncio.run(main.optimize_roadmap(payload))

        self.assertEqual(result["status"], "Success")
        self.assertEqual(len(result["roadmap"]), 4)
        self.assertIn("arm_index", result["metadata"])
        self.assertIn("population_size", result["metadata"])
        self.assertIn("mutation_rate", result["metadata"])

    def test_feedback_rejects_invalid_arm(self):
        payload = main.FeedbackRequest(arm_index=99, reward=1.0)

        with self.assertRaises(Exception) as err:
            asyncio.run(main.submit_feedback(payload))

        self.assertIn("Invalid arm_index", str(err.exception))


if __name__ == "__main__":
    unittest.main()
