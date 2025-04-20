import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def normalize_lambda(lam, lam_lerr, lam_uerr):
    lam_output, lam_lerr_output, lam_uerr_output = [], [], []

    for i in range(len(lam)):
        lambda_val = lam[i]
        if lambda_val < 0:
            lambda_val += 360
        if 0 <= lambda_val < 180:
            lam_output.append(lambda_val)
            lam_lerr_output.append(lam_lerr[i])
            lam_uerr_output.append(lam_uerr[i])
        else:
            lam_output.append(360 - lambda_val)
            lam_lerr_output.append(lam_uerr[i])
            lam_uerr_output.append(lam_lerr[i])

    return lam_output, lam_lerr_output, lam_uerr_output
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Catalog Viewer")
st.sidebar.markdown("# Catalog Viewer 📊")

st.markdown("""
    <style>
        .stApp, body {
            background-color: white !important;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv('obliquity.csv')

st.markdown("""
    <h2><span style="color: black;">RM</span><span style="color: red;">Cat</span>: Orbital Obliquity Measurements from Global Modeling to Rossiter-McLaughlin Effects</h2>
""", unsafe_allow_html=True)

lambdadeg, lambdadeg_uerr, lambdadeg_lerr = df['lambdadeg'].values, df['lambdadeg_uerr'].values, df['lambdadeg_lerr'].values
abslam, abslam_uerr, abslam_lerr = normalize_lambda(lambdadeg, lambdadeg_lerr, lambdadeg_uerr)
df['abslam'], df['abslam_uerr'], df['abslam_lerr'] = abslam, abslam_uerr, abslam_lerr

filtered_df = df.copy()

col1, col2 = st.columns([2, 1])

with col1:
    st.write(f"Showing {len(filtered_df)} entries (filtered from {len(df)} total entries)")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.markdown(r"""
    ### Summary Highlights
    <details>
    <summary> Hot Jupiter around Hot Stars can have High Obliquity: 7σ</summary>
    Mar 07, 2025: Updated README
    </details>
    <details>
    <summary> Single Star Warm Jupiter tend to be aligned: 3.5σ</summary>
    Mar 07, 2025: Updated README
    </details>
    <br/><br/>
    Last updated: 2025/04/19
    """, unsafe_allow_html=True)

with col2:
    st.subheader('Data Visualization')
    query_expr = st.text_area("Pandas filter for plot data (e.g., teff > 6000 & lambdadeg < 90):", 
                              value="abslam_uerr < 50 and abslam_lerr < 50 and abslam < 900 and Pflag == 'y' ", height=68)

    try:
        query_expr_single_line = " ".join(query_expr.strip().splitlines())
        plot_df = filtered_df.query(query_expr_single_line) if query_expr_single_line else filtered_df
    except Exception as e:
        st.error(f"Query error: {e}")
        plot_df = filtered_df

    if not plot_df.empty:
        numeric_columns = plot_df.select_dtypes(include='number').columns
        default_x = numeric_columns.get_loc('teff') if 'teff' in numeric_columns else 0
        default_y = numeric_columns.get_loc('abslam') if 'abslam' in numeric_columns else (1 if len(numeric_columns) > 1 else 0)

        x_axis = st.selectbox('Select X-axis', numeric_columns, index=default_x)
        y_axis = st.selectbox('Select Y-axis', numeric_columns, index=default_y)

        with st.expander("Advanced plot customization"):
            use_xerr = st.checkbox("Show X error bars", value=False)
            use_yerr = st.checkbox("Show Y error bars", value=False)
            marker_color = st.color_picker("Pick marker color", value="#ADD8E6")
            marker_symbol = st.selectbox("Select marker symbol", ["circle", "square", "diamond", "cross", "x", "triangle-up", "triangle-down"])
            marker_size = st.slider("Marker size", min_value=5, max_value=20, value=10)
            fig_title = st.text_input('Plot Title', value=f'{y_axis} vs {x_axis}')
            x_label = st.text_input('X-axis Label', value=x_axis)
            y_label = st.text_input('Y-axis Label', value=y_axis)

        hover_col = 'pl_name' if 'pl_name' in plot_df.columns else plot_df.columns[0]

        xerr_lower, xerr_upper = f"{x_axis}_lerr", f"{x_axis}_uerr"
        yerr_lower, yerr_upper = f"{y_axis}_lerr", f"{y_axis}_uerr"

        fig = go.Figure(data=go.Scatter(
            x=plot_df[x_axis], y=plot_df[y_axis], mode='markers',
            marker=dict(size=marker_size, color=marker_color, symbol=marker_symbol, line=dict(width=1, color='black')),
            text=plot_df[hover_col],
            hovertemplate=f"<b>%{{text}}</b><br>{x_axis}: %{{x}}<br>{y_axis}: %{{y}}",
            error_x=dict(type='data', symmetric=False, array=plot_df[xerr_upper] if use_xerr and xerr_upper in plot_df else None,
                         arrayminus=plot_df[xerr_lower] if use_xerr and xerr_lower in plot_df else None, color='rgba(0,0,0,0.3)'),
            error_y=dict(type='data', symmetric=False, array=plot_df[yerr_upper] if use_yerr and yerr_upper in plot_df else None,
                         arrayminus=plot_df[yerr_lower] if use_yerr and yerr_lower in plot_df else None, color='rgba(0,0,0,0.3)')
        ))

        fig.update_layout(title=fig_title, xaxis_title=x_label, yaxis_title=y_label)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for plotting.")
