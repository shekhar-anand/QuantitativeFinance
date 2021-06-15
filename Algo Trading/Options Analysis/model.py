from decimal import Decimal

PRECISION = Decimal(10) ** -2


class GreekValues:
    """
    This class is used for the defining values of different option greeks.
    """

    def __init__(self, callPrice, callDelta, callDelta2, callTheta, callRho, putPrice, putDelta, putDelta2, putTheta,
                 putRho, vega, gamma):
        """
        It initializes an instance which contains different greek values.
        :param callPrice: float
                Theoretical call price
        :param callDelta: float
                Call Delta
        :param callDelta2: float
                Call double delta
        :param callTheta: float
                Call Theta
        :param callRho: float
                Call Rho
        :param putPrice: float
                Theoretical put price
        :param putDelta: float
                Put Delta
        :param putDelta2: float
                Put double delta
        :param putTheta: float
                Put Theta
        :param putRho: float
                Put Rho
        :param vega: float
                Option vega
        :param gamma: float
                Option Gamma
        """
        self.call = callPrice
        self.call_delta = callDelta
        self.call_dual_delta = callDelta2
        self.call_theta = callTheta
        self.call_rho = callRho

        self.put = putPrice
        self.put_delta = putDelta
        self.put_dual_delta = putDelta2
        self.put_theta = putTheta
        self.put_rho = putRho

        self.vega = vega
        self.gamma = gamma


class StrikeEntry:
    """
    This is used to make a option's entry for analysis
    """

    def __init__(self, strike: int, option_type: str, signal: str = None, premium: float = None):
        """
        It creates an instance which refers to different properties of the option.
        :param strike: int
                    Strike price of the option
        :param option_type: str
                    Type of the option. Possible values CE and PE.
        :param signal: str
                    Signal for the option. Either 'buy' or 'sell'
        :param premium: float
                    Premium paid or received for the option.
        """
        self.strike = strike
        self.option_type = option_type
        self.signal = signal
        self.premium = premium

    def __str__(self) -> str:
        return "%s %s%s" % (self.signal, self.strike, self.option_type)
