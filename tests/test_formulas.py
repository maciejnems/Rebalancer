from unittest import TestCase

from rebalancer import formulas
from rebalancer.model import Token


class TestFormulas(TestCase):
    def test_amount_out(self):
        a_in = 10
        t_in = Token("in", 1100, 0.5, 1.0)
        t_out = Token("out", 1110, 0.5, 1.0)
        self.assertAlmostEqual(formulas.amount_out(a_in, t_in, t_out), 10.0)

        a_in = 50
        t_in = Token("in", 600, 0.6, 1.0)
        t_out = Token("out", 400, 0.4, 1.0)
        self.assertAlmostEqual(formulas.amount_out(
            a_in, t_in, t_out), 45.254551570268475)

    def test_amoun_in(self):
        a_out = 10.0
        t_in = Token("in", 1100, 0.5, 1.0)
        t_out = Token("out", 1110, 0.5, 1.0)
        self.assertAlmostEqual(formulas.amount_in(a_out, t_in, t_out), 10.0)

        a_in = 45.25455157
        t_in = Token("in", 600, 0.6, 1.0)
        t_out = Token("out", 400, 0.4, 1.0)
        self.assertAlmostEqual(formulas.amount_in(a_in, t_in, t_out), 50.0)

    def test_target_balances(self):
        tokens = {"a": Token("a", 650, 0.6, 1.0),
                  "b": Token("b", 354.74544842973154, 0.4, 1.0)}
        wanted_TB = {"a": 600, "b": 400}

        TB = formulas.target_balances(tokens)
        self.assertEqual(len(TB), 2)
        for name, tb in wanted_TB.items():
            self.assertAlmostEqual(
                TB[name], tb, msg=f'Target balance for {name} shoulf be {tb}, is {TB[name]}')

    def test_target_balance(self):
        tokens = {"a": Token("a", 650, 0.6, 1.0),
                  "b": Token("b", 354.74544842973154, 0.4, 1.0)}

        self.assertAlmostEqual(formulas.target_balance("a", tokens), 600)
        self.assertAlmostEqual(formulas.target_balance("b", tokens), 400)

    def test_new_target_ratios(self):
        diff = 200
        tokens = {"a": Token("a", 400, 0.5, 1.0),
                  "b": Token("b", 400, 0.5, 1.0)}
        wanted_ntr = {"a": 0.6, "b": 0.4}

        ntr = formulas.new_target_ratios("a", diff, tokens)
        self.assertEqual(len(ntr), 2)
        for name, tb in wanted_ntr.items():
            self.assertAlmostEqual(
                ntr[name], tb, msg=f'Target balance for {name} shoulf be {tb}, is {ntr[name]}')

    def test_get_issued(self):
        deposit = 200
        tokens = {"a": Token("a", 600, 0.6, 1.0),
                  "b": Token("b", 400, 0.4, 1.0)}

        self.assertAlmostEqual(formulas.get_issued("b", deposit, tokens), 200)

    def test_get_withdrawal(self):
        withdrawal = 200
        tokens = {"a": Token("a", 600, 0.6, 1.0),
                  "b": Token("b", 400, 0.4, 1.0)}

        self.assertAlmostEqual(formulas.get_withdrawal(
            "a", withdrawal, tokens), 200)

    def test_target_ratio(self):
        tokens = {"a": Token("a", 650, 0.4, 1.0),
                  "b": Token("b", 354.74544842973154, 0.2, 1.0),
                  "c": Token("c", 100.0, 0.4, 100.0)}
        trading_volumes = {
            "a": {"b": 100, "c": 200},
            "b": {"a": 100, "c": 100},
            "c": {"a": 200, "b": 100},
        }
        wanted_target_ratio = formulas.wanted_target_ratio(
            tokens, trading_volumes)

        self.assertAlmostEqual(wanted_target_ratio["a"], 0.3413795387586285)
        self.assertAlmostEqual(wanted_target_ratio["b"], 0.2425721937893485)
        self.assertAlmostEqual(wanted_target_ratio["c"], 0.4160482674520231)

    def test_new_target_ratios(self):
        tokens = {"a": Token("a", 400, 0.5, 1.0),
                  "b": Token("b", 400, 0.5, 1.0)}

        diff = formulas.deposit_to_change_ratio("a", 0.6, tokens)
        self.assertAlmostEqual(diff, 200)

        tokens = {"a": Token("a", 600, 0.6, 1.0),
                  "b": Token("b", 400, 0.4, 1.0)}

        diff = formulas.deposit_to_change_ratio("a", 0.5, tokens)
        self.assertAlmostEqual(diff, -200)
