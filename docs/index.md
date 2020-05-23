## Statewise Comparison of realtime *R<sub>t</sub>* and Growth rate of Confirmed cases

<iframe src="output.html" style="width:100%; height:550px;"></iframe>

![Scheduled Refresh of Data](https://github.com/Parijat29/COVID-19-India-R0-Analysis/workflows/Scheduled%20Refresh%20of%20Data/badge.svg)

*This chart refreshed multiple times each day and is in sync with current data.*

### What is *R<sub>t</sub>*?
In any epidemic, ![$R_t$](https://render.githubusercontent.com/render/math?math=%24R_t%24) is the measure known as the effective reproduction number. It's the number of people who become infected per infectious person at time ***t***. The most well-known version of this number is the basic reproduction number: ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) when ![$t=0$](https://render.githubusercontent.com/render/math?math=%24t%3D0%24). However, ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) is a single measure that does not adapt with changes in behavior and restrictions.

### How does it help?
As a pandemic evolves, increasing restrictions (or potential releasing of restrictions) changes ![$R_t$](https://render.githubusercontent.com/render/math?math=%24R_t%24). Knowing the current ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) is essential. When ![$R\gg1$](https://render.githubusercontent.com/render/math?math=%24R%5Cgg1%24), the pandemic will spread through a large part of the population. If ![$R_t\lt1$](https://render.githubusercontent.com/render/math?math=%24R_t%5Clt1%24), the pandemic will slow quickly before it has a chance to infect many people. The lower the ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24): the more manageable the situation. In general, any ![$R_t\lt1$](https://render.githubusercontent.com/render/math?math=%24R_t%5Clt1%24) means things are under control.

The value of ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) helps us in two ways. 
  1. It helps us understand how effective our measures have been controlling an outbreak
  2. it gives us vital information about whether we should increase or reduce restrictions based on our competing goals of economic prosperity and human safety. [Well-respected epidemiologists argue](https://www.nytimes.com/2020/04/06/opinion/coronavirus-end-social-distancing.html) that tracking *R<sub>t</sub>* is the only way to manage through this crisis.

### Limitations
  - Few States and United Territories might be missing in the chart. That is due to either insufficient data or very few confirmed cases in those areas.

### Credits
  - This work is based on [Estimating COVID-19's *R<sub>t</sub>* in Real-Time](https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb) By Kevin Systrom
  - Special thanks to [Thejesh GN](https://thejeshgn.com) for collecting and maintaining the State wise COVID-19 data from the [Ministry of Health and Family Welfare, Government of India](https://www.mohfw.gov.in/) website.

### Disclaimer
I'm not an Epidemiologist or scientist. I have only applied a modified version of a solution created by [Bettencourt & Ribeiro 2008](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0002185) to estimate real-time ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) using a Bayesian approach. While this paper estimates a static ***R*** value, here we introduce a process model with Gaussian noise to estimate a time-varying ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24).
