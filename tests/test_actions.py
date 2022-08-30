from unittest import TestCase

from rebalancer import actions, formulas
from rebalancer.model import Token


class TestActions(TestCase):
    def test_swap(self):
        tokens = {"a": Token("a", 650, 0.6, 1.0),
                  "b": Token("b", 354.74544842973154, 0.4, 1.0)}
        a_in = 45.254551570268475

        new_state = actions.swap(tokens, {}, a_in, "b", "a")
        self.assertAlmostEqual(new_state["a"].balance, 600 + 50 * formulas.SWAP_FEE)
        self.assertAlmostEqual(new_state["b"].balance, 400)

    def test_provide_liquidity(self):
        tokens = {"a": Token("a", 400, 0.5, 1.0),
                  "b": Token("b", 400, 0.5, 1.0)}
        deposit = 200
        user_registry = {}

        new_state = actions.provide_liquidity(
            tokens, user_registry, deposit, "a", "user")
        self.assertAlmostEqual(new_state["a"].balance, 600)
        self.assertAlmostEqual(new_state["a"].target_ratio, 0.6)
        self.assertAlmostEqual(new_state["a"].supply, 600)
        self.assertAlmostEqual(new_state["b"].balance, 400)
        self.assertAlmostEqual(new_state["b"].target_ratio, 0.4)
        self.assertAlmostEqual(new_state["b"].supply, 400)
        self.assertAlmostEqual(user_registry["user"]["a"], 200)

    def test_remove_liquidity(self):
        tokens = {"a": Token("a", 400, 0.5, 1.0),
                  "b": Token("b", 400, 0.5, 1.0)}
        deposit = 200
        user_registry = {}

        new_state = actions.provide_liquidity(
            tokens, user_registry, deposit, "a", "user")
        self.assertAlmostEqual(new_state["a"].balance, 600)
        self.assertAlmostEqual(new_state["a"].target_ratio, 0.6)
        self.assertAlmostEqual(new_state["a"].supply, 600)
        self.assertAlmostEqual(new_state["b"].balance, 400)
        self.assertAlmostEqual(new_state["b"].target_ratio, 0.4)
        self.assertAlmostEqual(new_state["b"].supply, 400)
        self.assertAlmostEqual(user_registry["user"]["a"], 200)

        new_state = actions.remove_liquidity(
            tokens, user_registry, deposit, "a", "user")
        self.assertAlmostEqual(new_state["a"].balance, 400)
        self.assertAlmostEqual(new_state["a"].target_ratio, 0.5)
        self.assertAlmostEqual(new_state["a"].supply, 400)
        self.assertAlmostEqual(new_state["b"].balance, 400)
        self.assertAlmostEqual(new_state["b"].target_ratio, 0.5)
        self.assertAlmostEqual(new_state["b"].supply, 400)
        self.assertAlmostEqual(user_registry["user"]["a"], 0)
