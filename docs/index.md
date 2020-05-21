## Statewise Comparison of realtime $R_t$ and Growth rate in Confirmed cases

<iframe src="output.html" width="950" height="550"></iframe>


### What is $R_t$?
In any epidemic, $R_t$ is the measure known as the effective reproduction number. It's the number of people who become infected per infectious person at time $t$. The most well-known version of this number is the basic reproduction number: $R_0$ when $t=0$. However, $R_0$ is a single measure that does not adapt with changes in behavior and restrictions.

### How does it help?
As a pandemic evolves, increasing restrictions (or potential releasing of restrictions) changes $R_t$. Knowing the current $R_t$ is essential. When $R\gg1$, the pandemic will spread through a large part of the population. If $R_t<1$, the pandemic will slow quickly before it has a chance to infect many people. The lower the $R_t$: the more manageable the situation. In general, any $R_t<1$ means things are under control.

The value of $R_t$ helps us in two ways. (1) It helps us understand how effective our measures have been controlling an outbreak and (2) it gives us vital information about whether we should increase or reduce restrictions based on our competing goals of economic prosperity and human safety. [Well-respected epidemiologists argue](https://www.nytimes.com/2020/04/06/opinion/coronavirus-end-social-distancing.html) that tracking $R_t$ is the only way to manage through this crisis.

### Credits
This work is based on [Estimating COVID-19's $R_t$ in Real-Time](https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb) By Kevin Systrom
Special thanks to [Thejesh GN](https://thejeshgn.com) for collecting and maintaining the State wise COVID-19 data from the [Ministry of Health and Family Welfare, Government of India](https://www.mohfw.gov.in/) website.

### Disclaimer
I'm not an Epidemiologist or scientist. I have only applied a modified version of a solution created by [Bettencourt & Ribeiro 2008](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0002185) to estimate real-time $R_t$ using a Bayesian approach. While this paper estimates a static $R$ value, here we introduce a process model with Gaussian noise to estimate a time-varying $R_t$.
