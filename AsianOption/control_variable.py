import numpy as np
import numpy.random as npr
from scipy.stats import norm
from AsianOption.asian_option import AsianOption
from AsianOption.displayer import DisplayerAsianOption

class ControlVariable(AsianOption):  # VAR (X) = VAR(X-Y+Y) <= VAR(X-Y) + VAR(Y)
    def __init__(self,r, s0, sigma, T, K, N, n):
        super().__init__(r, s0, sigma, T, K, N, n)

    def simulation_Path(self):
        r, S0, sigma, T, K, N, n = self.interest_rate, self.spot, self.sigma, self.maturity, self.Strike, self.MC_simulation, self.Time_step
        delta = float(T / n)
        G = npr.normal(0, 1, size=(N, n))
        # Log returns
        LR = (r - 0.5 * sigma ** 2) * delta + np.sqrt(delta) * sigma * G
        # concatenate with log(S0)
        LR = np.concatenate((np.log(S0) * np.ones((N, 1)), LR), axis=1)
        # cumsum horizontally (axis=1)
        LR = np.cumsum(LR, axis=1)
        # take the expo Spath matrix
        self.Spaths = np.exp(LR)
        return LR

    def Premium_by_control_variable_Y(self): #  controle variable Y = exp( 1/T * integrale_0_to_T ( log(Su) du )

        r, S0, sigma, T, K, N, n = self.interest_rate, self.spot, self.sigma, self.maturity, self.Strike, self.MC_simulation, self.Time_step
        LR = self.simulation_Path()
        Spaths = self.Spaths

        LR1 = LR[:, 0:len(Spaths[0, :]) - 1]
        Spaths = Spaths[:, 0:len(Spaths[0, :]) - 1]

        # take the average over each row
        Sbar1 = np.mean(LR1, axis=1)
        Sbar = np.mean(Spaths, axis=1)

        prix_vec = np.exp(-r * T) * np.maximum(Sbar - K, 0) - np.exp(Sbar1)
        Asian_MC_price = np.mean(prix_vec) + S0 * np.exp((r * T / 2) - (sigma ** 2) * T / 12)

        # 95% C.I

        sigma = np.std(prix_vec, ddof=1)  # standard deviation estimator

        error = 1.96 * sigma / np.sqrt(N)

        CI_up = Asian_MC_price + error

        CI_down = Asian_MC_price - error

        DisplayerAsianOption.displayPremium(Asian_MC_price, CI_down, CI_up, error, "Control variable Y")

        return Asian_MC_price, CI_down, CI_up

    @staticmethod
    def esperanceZ(r, S0, sigma, T, K):
        d = (np.log(K / S0) - (r - sigma ** 2 / 2) * T / 2) * (1 / sigma) * (np.sqrt(3 / T))
        E_Z = np.exp(-r * T) * ((S0 * np.exp((r - sigma ** 2 / 6) * T / 2) * norm.cdf(-d + sigma * np.sqrt(T / 3), 0,
                                                                                      1) - K * norm.cdf(-d, 0, 1)));

        return E_Z

    def Premium_by_control_variable_Z(self):  # controle variable Z = exp(-r T) * max ( exp( 1/T * integrale_0_to_T ( log(Su) du ) - K, 0 )

        r, S0, sigma, T, K, N, n = self.interest_rate, self.spot, self.sigma, self.maturity, self.Strike, self.MC_simulation, self.Time_step
        LR = self.simulation_Path()
        Spaths = self.Spaths

        LR1 = LR[:, 0:len(Spaths[0, :]) - 1]
        Spaths = Spaths[:, 0:len(Spaths[0, :]) - 1]

        # take the average over each row
        Sbar1 = np.mean(LR1, axis=1)
        Sbar = np.mean(Spaths, axis=1)

        prix_vec = np.exp(-r * T) * np.maximum(Sbar - K, 0) - np.exp(-r * T) * np.maximum(np.exp(Sbar1) - K, 0)

        Asian_MC_price = np.mean(prix_vec) + ControlVariable.esperanceZ(r, S0, sigma, T, K)

        # 95% C.I
        sigma = np.std(prix_vec, ddof=1)  # standard deviation estimator
        error = 1.96 * sigma / np.sqrt(N)
        CI_up = Asian_MC_price + error
        CI_down = Asian_MC_price - error

        DisplayerAsianOption.displayPremium(Asian_MC_price, CI_down, CI_up, error, "Control variable Z")

        return Asian_MC_price, CI_down, CI_up
