import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats as sps
from scipy.interpolate import interp1d
import requests
from plotly.subplots import make_subplots
from sklearn import preprocessing
from datetime import date

import plotly
# plotly.offline.init_notebook_mode(connected=True)

FILTERED_REGION_CODES = []

R_T_MAX = 12
r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)

# Gamma is 1/serial interval
# https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article
# https://www.nejm.org/doi/full/10.1056/NEJMoa2001316
GAMMA = 1/7

state_codes = {
    'KL' : 'Kerala',
    'DL' : 'Delhi',
    'TG' : 'Telengana',
    'RJ' : 'Rajasthan',
    'HR' : 'Haryana',
    'JK' : 'Jammu and Kashmir',
    'KA' : 'Karnataka',
    'LA' : 'Lakshadweep Islands',
    'MH' : 'Maharashtra',
    'PB' : 'Punjab',
    'TN' : 'Tamil Nadu',
    'UP' : 'Uttar Pradesh',
    'AP' : 'Andhra Pradesh',
    'UT' : 'Uttarakhand',
    'OR' : 'Odisha',
    'WB' : 'West Bengal',
    'PY' : 'Pondicherry',
    'CH' : 'Chandigarh',
    'CT' : 'Chattisgarh',
    'GJ' : 'Gujarat',
    'HP' : 'Himachal Pradesh',
    'MP' : 'Madhya Pradesh',
    'BR' : 'Bihar',
    'MN' : 'Manipur',
    'MZ' : 'Mizoram',
    'GA' : 'Goa',
    'AN' : 'Andaman and Nicobar Islands',
    'AS' : 'Assam',
    'JH' : 'Jharkhand',
    'AR' : 'Arunachal Pradesh',
    'TR' : 'Tripura',
    'NL' : 'Nagaland',
    'ML' : 'Meghalaya',
    'DN' : 'Dadra and Nagar Haveli'
}

def highest_density_interval(pmf, p=.9, debug=False):
    # If we pass a DataFrame, just call this recursively on the columns
    if(isinstance(pmf, pd.DataFrame)):
        return pd.DataFrame([highest_density_interval(pmf[col], p=p) for col in pmf],
                            index=pmf.columns)
    
    cumsum = np.cumsum(pmf.values)
    
    # N x N matrix of total probability mass for each low, high
    total_p = cumsum - cumsum[:, None]
    
    # Return all indices with total_p > p
    lows, highs = (total_p > p).nonzero()
    
    # Find the smallest range (highest density)
    best = (highs - lows).argmin()
    
    low = pmf.index[lows[best]]
    high = pmf.index[highs[best]]
    
    return pd.Series([low, high],
                     index=[f'Low_{p*100:.0f}',
                            f'High_{p*100:.0f}'])

def prepare_cases(cases, cutoff=1):
    new_cases = cases.diff()

    smoothed = new_cases.rolling(7,
        win_type='gaussian',
        min_periods=1,
        center=True).mean(std=2).round()
    
    idx_start = np.searchsorted(smoothed, cutoff)
    
    smoothed = smoothed.iloc[idx_start:]
    original = new_cases.loc[smoothed.index]
    
    return original, smoothed

def get_posteriors(sr, sigma=0.15):

    # (1) Calculate Lambda
    lam = sr[:-1].values * np.exp(GAMMA * (r_t_range[:, None] - 1))

    
    # (2) Calculate each day's likelihood
    likelihoods = pd.DataFrame(
        data = sps.poisson.pmf(sr[1:].values, lam),
        index = r_t_range,
        columns = sr.index[1:])
    
    # (3) Create the Gaussian Matrix
    process_matrix = sps.norm(loc=r_t_range,
                              scale=sigma
                             ).pdf(r_t_range[:, None]) 

    # (3a) Normalize all rows to sum to 1
    process_matrix /= process_matrix.sum(axis=0)
    
    # (4) Calculate the initial prior
    #prior0 = sps.gamma(a=4).pdf(r_t_range)
    prior0 = np.ones_like(r_t_range)/len(r_t_range)
    prior0 /= prior0.sum()

    # Create a DataFrame that will hold our posteriors for each day
    # Insert our prior as the first posterior.
    posteriors = pd.DataFrame(
        index=r_t_range,
        columns=sr.index,
        data={sr.index[0]: prior0}
    )
    
    # We said we'd keep track of the sum of the log of the probability
    # of the data for maximum likelihood calculation.
    log_likelihood = 0.0

    # (5) Iteratively apply Bayes' rule
    last_denominator = 0
    for previous_day, current_day in zip(sr.index[:-1], sr.index[1:]):

        #(5a) Calculate the new prior
        current_prior = process_matrix @ posteriors[previous_day]
        
        #(5b) Calculate the numerator of Bayes' Rule: P(k|R_t)P(R_t)
        numerator = likelihoods[current_day] * current_prior
        
        #(5c) Calcluate the denominator of Bayes' Rule P(k)
        denominator = np.sum(numerator)
        # Execute full Bayes' Rule
        
        if denominator == 0:
            posteriors[current_day] = posteriors[previous_day]
            log_likelihood += np.log(last_denominator)
        else:
            posteriors[current_day] = numerator/denominator        
            # Add to the running sum of log likelihoods
            log_likelihood += np.log(denominator)
            last_denominator = denominator
    
    return posteriors, log_likelihood


r = requests.get('https://raw.githubusercontent.com/datameet/covid19/master/data/mohfw.json')
x = r.json()
states_data = pd.DataFrame([row['value'] for row in x['rows']])
states_data['state'] = states_data['state'].str.upper()
states_data['date'] = pd.to_datetime(states_data['report_time'], utc=True)
states_data.drop(['_id', '_rev', 'report_time', 'confirmed_india', 'confirmed_foreign', 'source', 'type'], axis=1, inplace=True)
states = states_data[['date', 'state', 'confirmed']]
states = states.set_index(['state', 'date']).sort_index()
states = states.squeeze(axis=1)

sigmas = np.linspace(1/20, 1, 20)

targets = ~states.index.get_level_values('state').isin(FILTERED_REGION_CODES)
states_to_process = states.loc[targets]

results = {}

for state_name, cases in states_to_process.groupby(level='state'):
    
    print(state_name)
    new, smoothed = prepare_cases(cases, cutoff=10)
    
    if len(smoothed) == 0:
        new, smoothed = prepare_cases(cases, cutoff=1)
    
    if len(smoothed) == 0:
        FILTERED_REGION_CODES.append(state_name)
        continue
    
    result = {}
    
    # Holds all posteriors with every given value of sigma
    result['posteriors'] = []
    
    # Holds the log likelihood across all k for each value of sigma
    result['log_likelihoods'] = []
    
    for sigma in sigmas:
        posteriors, log_likelihood = get_posteriors(smoothed, sigma=sigma)
        result['posteriors'].append(posteriors)
        result['log_likelihoods'].append(log_likelihood)
    
    # Store all results keyed off of state name
    results[state_name] = result
    # clear_output(wait=True)

print('Done.')

total_log_likelihoods = np.zeros_like(sigmas)

# Loop through each state's results and add the log likelihoods to the running total.
for state_name, result in results.items():
    total_log_likelihoods += result['log_likelihoods']

# Select the index with the largest log likelihood total
max_likelihood_index = total_log_likelihoods.argmax()

# Select the value that has the highest log likelihood
sigma = sigmas[max_likelihood_index]

final_results = None

for state_name, result in results.items():
    print(state_name)
    posteriors = result['posteriors'][max_likelihood_index]
    hdis_90 = highest_density_interval(posteriors, p=.9)
    hdis_50 = highest_density_interval(posteriors, p=.5)
    most_likely = posteriors.idxmax().rename('ML')
    result = pd.concat([most_likely, hdis_90, hdis_50], axis=1)
    if final_results is None:
        final_results = result
    else:
        final_results = pd.concat([final_results, result])
    # clear_output(wait=True)

print('Done.')

def make_r0_fig(result, visible=True):
    scatter_plot = go.Scatter(
                x=result.reset_index(level=0).index, 
                y=result.reset_index(level=0)['ML'], 
                mode='lines+markers',
                line=dict(color='rgb(50,50,50)', width=1),
                marker=dict(
                    size=8,
                    color=result['ML'], #set color equal to a variable
                    colorscale=["black", "rgb(200,200,200)", "red"], # one of plotly colorscales
                    cmin=0,
                    cmid=1,
                    cmax=2,
                    line_width=1
                ),
                name='r0 value',
                visible = visible
            )
    return scatter_plot

def make_low_90_fig(result, visible=True):
    scatter_plot = go.Scatter(
                x=result.reset_index(level=0).index, 
                y=result.reset_index(level=0)['Low_90'], 
                mode='lines',
                line=dict(color='rgb(180,180,180)', width=1),
                name='r0 - low 90 value',
                visible = visible
            )
    return scatter_plot

def make_high_90_fig(result, visible=True):
    scatter_plot = go.Scatter(
                x=result.reset_index(level=0).index, 
                y=result.reset_index(level=0)['High_90'], 
                mode='lines',
                line=dict(color='rgb(180,180,180)', width=1),
                name='r0 - high 90 value',
                fill='tonexty',
                visible = visible
            )
    return scatter_plot

def make_log_plot(state_name, visible=True):
    state_data = states_data[states_data['state'] == state_name]
    log_transformer = preprocessing.FunctionTransformer(np.log, validate=True)
    confirmed_log = log_transformer.fit_transform(state_data['confirmed'].values.reshape(-1, 1))
    return go.Scatter(x=state_data['date'], y=confirmed_log.ravel(), mode='lines', 
                            line=dict(color='cornflowerblue', width=1.5),
                            name='Confirmed cases',
                            visible = visible
                        )

fig = make_subplots(rows=1, cols=2)
updatemenu=[]
buttons=[]
visibility = [False] * len(final_results.groupby('state')) * 4
for i, (state_name, result) in enumerate(final_results.groupby('state')):
    try:
        if i == 0:
            fig.add_trace(make_low_90_fig(result), row=1, col=1)
            fig.add_trace(make_high_90_fig(result), row=1, col=1)
            fig.add_trace(make_r0_fig(result), row=1, col=1)
            fig.add_trace(make_log_plot(state_name), row=1, col=2)
        else:
            fig.add_trace(make_low_90_fig(result, False), row=1, col=1)
            fig.add_trace(make_high_90_fig(result, False), row=1, col=1)
            fig.add_trace(make_r0_fig(result, False), row=1, col=1)
            fig.add_trace(make_log_plot(state_name, False), row=1, col=2)

        temp_visible = visibility.copy()
        temp_visible[i*4] = True
        temp_visible[i*4 + 1] = True
        temp_visible[i*4 + 2] = True
        temp_visible[i*4 + 3] = True
        buttons.append(dict(label=state_codes[state_name],
                            method = 'update',
                            args = [{'visible': temp_visible}]),
                        )
    except:
        continue

updatemenus = [
    dict(
        direction="down",
        showactive=True,
        pad={"r": 10, "t": 10},
        buttons=buttons,
        x=0.5,
        xanchor="center",
        y=1.2,
        yanchor="bottom"
    )
]

annotations = []
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.2,
                              xanchor='center', yanchor='top',
                              text=f'Last Updated on: {date.today()} ; Source: Data from MoHFW, maintained by Thejesh GN',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(180,180,180)'),
                              showarrow=False))

annotations.append(dict(xref='paper', yref='paper', x=0.23, y=1.05,
                              xanchor='center', yanchor='bottom',
                              text='Realtime Rt',
                              font=dict(family='Arial',
                                        size=20,
                                        color='rgb(50,50,50)'),
                              showarrow=False))
annotations.append(dict(xref='paper', yref='paper', x=0.77, y=1.05,
                              xanchor='center', yanchor='bottom',
                              text='Growth rate of cumulative cases',
                              font=dict(family='Arial',
                                        size=20,
                                        color='rgb(50,50,50)'),
                              showarrow=False))

fig.update_layout(
    autosize=False,
    width=900,
    height=500,
    margin=dict(
        l=40,
        r=40,
        b=100,
        t=100,
        pad=4
    ),
    showlegend=False, updatemenus=updatemenus, annotations=annotations
)

fig.update_yaxes(range=[0, 9], col=1)
fig.update_yaxes(range=[0, 1.1], type="log", col=2)
# fig.show()
fig.write_html("output.html", include_plotlyjs='cdn', full_html='false')