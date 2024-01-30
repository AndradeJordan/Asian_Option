
from AsianOption import asian_option,control_variable

def main():
    r, S0, sigma, T, K, N, n = 0.05,100,0.2,1,95,10000,100

    # Asian's PayOff by Riemann approximation
    my_AsianOption = asian_option.AsianOption(r, S0, sigma, T, K, N, n)
    _,_,_ = my_AsianOption.premium_by_riemann_approximation()

    # Asian's PayOff by Trapèze approximation
    _,_,_ = my_AsianOption.premium_by_trapeze_approximation()

    # Asian's PayOff by Control variable Y and Z :
    my_AsianOption_by_control_variable = control_variable.ControlVariable(r, S0, sigma, T, K, N, n)

    #  controle variable Y = exp( 1/T * integrale_0_to_T ( log(Su) du )
    _,_,_ = my_AsianOption_by_control_variable.Premium_by_control_variable_Y()

    # controle variable Z = exp(-r T) * max ( exp( 1/T * integrale_0_to_T ( log(Su) du ) - K, 0 )
    _,_,_ = my_AsianOption_by_control_variable.Premium_by_control_variable_Z()


if __name__ == "__main__":
    main()