
class DisplayerAsianOption:
    @staticmethod
    def displayPremium(payoff, lower_bound, upper_bound,error,tag):
        print("By "+tag+" approximation : ")
        print('autocollable\'s payoff (%)  : ', payoff)
        print('Error : ', error)
        print('confidence Interval (%): [', lower_bound, ',', upper_bound, ']')
