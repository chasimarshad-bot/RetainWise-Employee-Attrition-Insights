"""Consistent labelled Plotly views with aggregate-only browser payloads."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from textwrap import wrap
from .analysis import MIN_GROUP, distribution

TEAL = '#137C72'
AMBER = '#A85B18'
COLORS = {'Retained': TEAL, 'Attrited': AMBER}


def finish(fig, title, x, y):
    fig.update_layout(title=dict(text='<br>'.join(wrap(title, width=38)), font_size=17), xaxis_title=x, yaxis_title=y,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial, sans-serif', size=13, color='#172D3B'),
        margin=dict(l=15, r=15, t=65, b=35), height=355,
        legend_title_text='Employee outcome', hoverlabel=dict(bgcolor='white'))
    fig.update_yaxes(gridcolor='#DEE6EA', zeroline=False)
    fig.update_xaxes(tickfont=dict(color='#415967'))
    fig.update_yaxes(tickfont=dict(color='#415967'))
    return fig


def rates(table, field, title):
    """Only reviewed aggregates and explicit group sizes enter the figure."""
    visible = table.dropna(subset=['rate_pct']).copy()
    visible[field] = visible[field].astype(str)
    fig = px.bar(visible, x=field, y='rate_pct', text='rate_pct',
        custom_data=['n', 'attrited', 'caution'], color_discrete_sequence=[TEAL])
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside', cliponaxis=False,
        hovertemplate='%{x}<br>Attrition: %{y:.2f}%<br>Employees: %{customdata[0]}<br>Attrited: %{customdata[1]}<br>%{customdata[2]}<extra></extra>')
    maximum = visible.rate_pct.max() if len(visible) else 0
    fig.update_yaxes(range=[0, min(105, max(25, maximum * 1.25))], ticksuffix='%')
    return finish(fig, title, field, 'Observed attrition rate (%)')


def outcomes(df):
    counts = df.Status.value_counts().reindex(['Retained', 'Attrited'], fill_value=0)
    fig = px.bar(x=counts.index, y=counts.values, text=counts.values,
        color=counts.index, color_discrete_map=COLORS)
    fig.update_traces(hovertemplate='%{x}<br>Employees: %{y}<extra></extra>', textposition='outside', cliponaxis=False)
    fig.update_yaxes(range=[0, max(1, counts.max()) * 1.2])
    fig.update_layout(showlegend=False)
    return finish(fig, 'Recorded employee outcomes', 'Employee outcome', 'Employees')


def boxes(df, field, label):
    """Precompute box statistics so no employee-level rows are sent to the browser."""
    fig = go.Figure()
    for row in distribution(df, field).to_dict('records'):
        if row['n'] < MIN_GROUP:
            continue
        values = df.loc[df.Status == row['Status'], field]
        iqr = row['q3'] - row['q1']
        inside = values[values.between(row['q1'] - 1.5 * iqr, row['q3'] + 1.5 * iqr)]
        name = f"{row['Status']} (n={row['n']})"
        fig.add_trace(go.Box(name=name, x=[name], q1=[row['q1']],
            median=[row['median']], q3=[row['q3']], lowerfence=[inside.min()],
            upperfence=[inside.max()], boxpoints=False, marker_color=COLORS[row['Status']]))
    fig.update_layout(showlegend=False)
    return finish(fig, f'{label} by employee outcome', 'Employee outcome', label)


def histogram(df, field, label, bins=12):
    """Use shared bins and group percentages to compare unequal outcome sizes."""
    import numpy as np
    fig = go.Figure()
    edges = np.histogram_bin_edges(df[field], bins=bins)
    for status, group in df.groupby('Status'):
        if len(group) < MIN_GROUP:
            continue
        counts, _ = np.histogram(group[field], bins=edges)
        labels = [f'{a:g}–{b:g}' for a, b in zip(edges[:-1], edges[1:])]
        fig.add_trace(go.Bar(name=f'{status} (n={len(group)})', x=labels,
            y=100 * counts / len(group), marker_color=COLORS[status],
            marker_pattern_shape='/' if status == 'Attrited' else '',
            customdata=counts, hovertemplate='%{x}<br>Within-outcome share: %{y:.1f}%<br>Employees in bin: %{customdata}<extra>%{fullData.name}</extra>'))
    fig.update_layout(barmode='group')
    return finish(fig, f'How {label.lower()} is distributed', label + ' (shared bins)', 'Share within outcome (%)')
