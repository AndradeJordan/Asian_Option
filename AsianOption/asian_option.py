from absProduct import AbsProduct
from AsianOption.displayer import DisplayerAsianOption
import numpy as np
import numpy.random as npr

class AsianOption(AbsProduct):
    def __init__(self,r, s0, sigma, T, K, N, n):
        self.interest_rate, self.spot, self.sigma, self.maturity = r, s0, sigma, T
        self.Strike, self.MC_simulation, self.Time_step = K, N, n
        self.Spaths = None

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


    def premium_by_riemann_approximation(self):
        r, S0, sigma, T, K, N, n = self.interest_rate, self.spot, self.sigma, self.maturity, self.Strike, self.MC_simulation, self.Time_step
        self.simulation_Path()

        Spaths = self.Spaths

        # initial and end p_values
        fa = Spaths[:, 0]
        fb = Spaths[:, n - 1]

        ## Riemann approximation
        # remove final time component
        Spaths = Spaths[:, 0:len(Spaths[0, :]) - 1]
        # print(Spaths)
        # take the average over each row
        Sbar = np.mean(Spaths, axis=1)
        # print(Sbar)
        payoff = np.exp(-r * T) * np.maximum(Sbar - K, 0)  # call function
        Asian_MC_price_R = np.mean(payoff)
        # 95% C.I
        sigma = np.std(payoff)  # standard deviation estimator : ecart type de monte_carlo
        error = 1.96 * sigma / np.sqrt(N)
        CI_up_R = Asian_MC_price_R + error
        CI_down_R = Asian_MC_price_R - error
        DisplayerAsianOption.displayPremium(Asian_MC_price_R, CI_down_R, CI_up_R, error, "Riemann")

        return Asian_MC_price_R, CI_down_R, CI_up_R

    def premium_by_trapeze_approximation(self):
        r, S0, sigma, T, K, N, n = self.interest_rate, self.spot, self.sigma, self.maturity, self.Strike, self.MC_simulation, self.Time_step
        self.simulation_Path()

        Spaths = self.Spaths

        # initial and end p_values
        fa = Spaths[:, 0]
        fb = Spaths[:, n - 1]

        spathsTRAP = Spaths[:, 1:len(Spaths[0, :])]
        Sbar1 = np.cumsum(spathsTRAP, axis=1)[:, n - 2]

        SbarTRAP = (Sbar1 + (fa + fb) * 0.5) / n
        payoff1 = np.exp(-r * T) * np.maximum(SbarTRAP - K, 0)  # call function
        Asian_MC_price_T = np.mean(payoff1)
        # 95% CI SbarTRAP
        sigma1 = np.std(payoff1)  # standard deviation estimator : ecart type de monte_carlo
        error_T = 1.96 * sigma1 / np.sqrt(N)
        CI_up_T = Asian_MC_price_T + error_T
        CI_down_T = Asian_MC_price_T - error_T
        DisplayerAsianOption.displayPremium(Asian_MC_price_T, CI_down_T, CI_up_T, error_T, "Trapeze")

        return Asian_MC_price_T, CI_down_T, CI_up_T




