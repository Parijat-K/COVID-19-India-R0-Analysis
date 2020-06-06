COVID-19 Statewise R0 Analysis for India
===
[Link to Dashboard](https://parijat29.github.io/COVID-19-India-R0-Analysis/)

### Data Refresh
The chart is generated daily multiple times using GitHub actions. It is scheduled to run every 6th hour as per UTC timezone.
![Scheduled Refresh of Data](https://github.com/Parijat29/COVID-19-India-R0-Analysis/workflows/Scheduled%20Refresh%20of%20Data/badge.svg)

### What is *R<sub>t</sub>*?
In any epidemic, ![$R_t$](https://render.githubusercontent.com/render/math?math=%24R_t%24) is the measure known as the effective reproduction number. It's the number of people who become infected per infectious person at time ***t***. The most well-known version of this number is the basic reproduction number: ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) when ![$t=0$](https://render.githubusercontent.com/render/math?math=%24t%3D0%24). However, ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) is a single measure that does not adapt with changes in behavior and restrictions.

### How does it help?
As a pandemic evolves, increasing restrictions (or potential releasing of restrictions) changes ![$R_t$](https://render.githubusercontent.com/render/math?math=%24R_t%24). Knowing the current ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) is essential. When ![$R\gg1$](https://render.githubusercontent.com/render/math?math=%24R%5Cgg1%24), the pandemic will spread through a large part of the population. If ![$R_t\lt1$](https://render.githubusercontent.com/render/math?math=%24R_t%5Clt1%24), the pandemic will slow quickly before it has a chance to infect many people. The lower the ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24): the more manageable the situation. In general, any ![$R_t\lt1$](https://render.githubusercontent.com/render/math?math=%24R_t%5Clt1%24) means things are under control.

The value of ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) helps us in two ways. 
  1. It helps us understand how effective our measures have been controlling an outbreak
  2. it gives us vital information about whether we should increase or reduce restrictions based on our competing goals of economic prosperity and human safety. [Well-respected epidemiologists argue](https://www.nytimes.com/2020/04/06/opinion/coronavirus-end-social-distancing.html) that tracking *R<sub>t</sub>* is the only way to manage through this crisis.

### Limitations
  - Few States and United Territories might be missing in the chart. That is due to either insufficient data or very few confirmed cases in those areas.
  
News Coverage
---
This work was cited in the below news
* [How dangerous is COVID-19 in the grand scheme of things](https://www.deccanherald.com/science-and-environment/how-dangerous-is-covid-19-in-the-grand-scheme-of-things-845993.html), [Deccan Herald](https://www.deccanherald.com/)  
* [Covid slowing in Maharashtra and MP, shows infection rate analysis of govt data](https://theprint.in/health/covid-slowing-in-maharashtra-and-mp-shows-infection-rate-analysis-of-govt-data/436861/), [The Print](https://theprint.in/)

Social Media Coverage
---
This work has been appreciated in social media by epidologists and public health professionals-
* [Dr. Giridhar R Babu, Professor, Head, Life course Epidemiology, Physician](https://twitter.com/epigiri/status/1266424638592053248)
* [Lipika Nanda, Vice President, Multisectoral Planning in Health, PHFI. Public Health Professional](https://twitter.com/NandaLipika/status/1266779511091126273)

### Credits
  - This work is based on [Estimating COVID-19's *R<sub>t</sub>* in Real-Time](https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb) By [Kevin Systrom](https://github.com/k-sys)
  - Special thanks to [Thejesh GN](https://thejeshgn.com) for collecting and maintaining the State wise COVID-19 data from the [Ministry of Health and Family Welfare, Government of India](https://www.mohfw.gov.in/) website.

### Disclaimer
I'm not an Epidemiologist or scientist. I have only applied a modified version of a solution created by [Bettencourt & Ribeiro 2008](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0002185) to estimate real-time ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24) using a Bayesian approach. While this paper estimates a static ***R*** value, here we introduce a process model with Gaussian noise to estimate a time-varying ![$R_0$](https://render.githubusercontent.com/render/math?math=%24R_0%24).
