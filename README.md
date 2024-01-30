# Definition

I study Pricing of Asian options and variance reduction on the Black-Sholes model : 
$$S_t= S_0\exp((r-\frac{\sigma^2}{2})t + \sigma W_t)$$ 

And I simulate the price of the Asian option $\mathbb{E}[e^{-rT}(\frac{1}{T} \int_0^{T} S_t\,dt - K)_+]$ by the Monte Carlo method with different schemes, show the importance of variance reduction for the calculation of the price.

The parameters of Asian option are:

- **An underlying S**
- **Interest rate r**
- **Strike K**
- **A maturity T**
- **Volatility $\sigma$**

# Asian option pricing approximations methods
If we want to simulate the price of the Asian option by Monte Carlo methods,
we must approach the integral $\int_0^{T} S_t\,dt$ , where $S_t$ can exactly be simulated.

- **Riemann's approximation** : $$\frac{1}{T}\int_0^{T} S_t\,dt  = \frac{1}{n}\sum_{k=0}^{n-1} S_{t_k}$$
- **Trapeze's approximation** : $$\frac{1}{T}\int_0^{T} S_t\,dt  = \frac{1}{n}\sum_{k=0}^{n-1} \frac{S_{t_{k+1}}+S_{t_k}}{2}
        = \frac{1}{n}(\frac{S_0 + S_{t_n}}{2} + \sum_{k=1}^{n-1} S_{t_k})$$



# Control Variable
In this part, in order to improve the efficiency of the Monte Carlo simulation, 
we will perform a variance reduction by control variables that are  $Y= \exp(\frac{1}{T}\int_0^{T} \log(S_u)\,du)$ and
$Z= e^{-rT}(e^{\frac{1}{T}\int_0^{T} \log(S_u)\,du} - K)_+$ where :

- $$\mathbb{E}(Y) = S_0 e^{r\frac{T}{2} - \sigma^{2}\frac{T}{4}}$$.
- $$\mathbb{E}(Z) = e^{-rT}[-KN(-d)+S_0e^{(r-\frac{\sigma^2}{6})\frac{T}{2}}N(-d+\sigma\sqrt{\frac{T}{3}})]$$

If you compile the code you will see that the error decreased with the variable Y but it decreased even more with the variable Z. 
These two variables have therefore reduced the variance. 
The confidence interval "narrows" and we get even closer to the real price which is 8.82

# Conclusion 

With the Black Scholes model, I was able to price the Asian option without reduction of variation with three numerical methods of integral approximation. 
However, the prices obtained were not too close to the real price. 
So I used very effective control variables that allowed me to reduce the confidence interval.