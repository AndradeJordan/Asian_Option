import unittest
from AsianOption import asian_option,control_variable

class MyTestCase(unittest.TestCase):
    def test_something(self):
        # Asian's PayOff by Riemann approximation
        r, S0, sigma, T, K, N, n = 0.05, 100, 0.2, 1, 95, 10000, 100
        True_price = 8.82
        my_AsianOption = asian_option.AsianOption(r, S0, sigma, T, K, N, n)
        price, lower_bound, upper_bound = my_AsianOption.premium_by_riemann_approximation()
        #self.assertEqual(price, True_price)    #   we can't find the exact value of an Asian Option
        self.assertAlmostEqual(price, True_price, delta=1e-1)
        self.assertGreaterEqual(price, lower_bound)
        self.assertLessEqual(price, upper_bound)

        # Asian's PayOff by Trapèze approximation
        price, lower_bound, upper_bound = my_AsianOption.premium_by_trapeze_approximation()
        #self.assertEqual(price, True_price)
        self.assertAlmostEqual(price, True_price, delta=1e-1)
        self.assertGreaterEqual(price, lower_bound)
        self.assertLessEqual(price, upper_bound)

        # Asian's PayOff by Control variable Y and Z :
        my_AsianOption_by_control_variable = control_variable.ControlVariable(r, S0, sigma, T, K, N, n)
        #self.assertEqual(price, True_price)
        self.assertAlmostEqual(price, True_price, delta=1e-1)
        self.assertGreaterEqual(price, lower_bound)
        self.assertLessEqual(price, upper_bound)

        #  controle variable Y = exp( 1/T * integrale_0_to_T ( log(Su) du )
        price, lower_bound, upper_bound = my_AsianOption_by_control_variable.Premium_by_control_variable_Y()
        #self.assertEqual(price, True_price)
        self.assertAlmostEqual(price, True_price, delta=1e-1)
        self.assertGreaterEqual(price, lower_bound)
        self.assertLessEqual(price, upper_bound)

        # controle variable Z = exp(-r T) * max ( exp( 1/T * integrale_0_to_T ( log(Su) du ) - K, 0 )
        price, lower_bound, upper_bound = my_AsianOption_by_control_variable.Premium_by_control_variable_Z()
        #self.assertEqual(price, True_price)
        self.assertAlmostEqual(price, True_price, delta=1e-1)
        self.assertGreaterEqual(price, lower_bound)
        self.assertLessEqual(price, upper_bound)



if __name__ == '__main__':
    unittest.main()
