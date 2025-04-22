import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


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

import base64

# Convert local image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

image_base64 = get_base64_image("logo.png")

st.markdown(f"""
    <h2>
        <img src="{image_base64}" alt="RMcat Logo" style="height: 60px; vertical-align: middle; margin-right: 10px;">
        <span style="color: black;">RM</span><span style="color: red;">Cat</span>: Stellar Obliquity Measurements from Global Modeling to Rossiter-McLaughlin Effects
    </h2>
    <details>
        <summary>About</summary>
        <p>RMcat is a catalog of stellar obliquity measurements from global modeling to Rossiter-McLaughlin effects. It includes data from various sources and provides a comprehensive overview of the current state of research in this field.</p>
    </details>
""", unsafe_allow_html=True)


# array(['System', 'st_teff', 'st_teff_uerr', 'st_teff_lerr', 'Pflag',
#        'pl_projobliq', 'pl_projobliq_uerr', 'pl_projobliq_lerr', 'st_psi',
#        'st_psi_uerr', 'st_psi_lerr', 'pl_letter', 'st_name', 'tic_id',
#        'pl_ratdor', 'pl_ratdor_uerr', 'pl_ratdor_lerr', 'pl_bmassj',
#        'pl_bmassj_uerr', 'pl_bmassj_lerr', 'pl_orbeccen',
#        'pl_orbeccen_uerr', 'pl_orbeccen_lerr', 'st_mass', 'st_mass_uerr',
#        'st_mass_lerr', 'st_radius', 'st_radius_uerr', 'st_radius_lerr',
#        'st_mratio', 'st_mratio_uerr', 'st_mratio_lerr', 'Binary',
#        'Ref_link', 'controversial', 'pl_projobliqabs',
#        'pl_projobliqabs_uerr', 'pl_projobliqabs_lerr'], dtype=object)

pars2label = {'pl_projobliqabs': 'Sky-projected obliquity (degrees)',
              'st_teff': 'Stellar effective temperature (K)',
              'st_mass': 'Stellar mass (M☉)',
                'st_radius': 'Stellar radius (R☉)',
                'pl_bmassj': 'Planet mass (Jupiter mass)',
                'pl_orbeccen': 'Orbital eccentricity',
                'pl_ratdor': 'Semi-major axis / stellar radius',
                'st_psi': 'True stellar obliquity (degrees)',
                'pl_projobliq': 'Sky-projected obliquity (degrees)',
                'st_mratio': 'Stellar mass ratio'}


filtered_df = df.copy()

col1, col2 = st.columns([2, 1])

with col1:
    st.write(f"Showing {len(filtered_df)} entries (filtered from {len(df)} total entries)")
    # st.markdown("### Interactive Data Table (Filter like Excel)")

    from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filter=True, sortable=True, resizable=True)
    if "System" in df.columns:
        gb.configure_column("System", pinned="left")
    # gb.configure_grid_options(domLayout='normal') 
    gb.configure_grid_options(autoSizeAllColumns=True)

    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        enable_enterprise_modules=False,
        height=500,
        width='100%',
        allow_unsafe_jscode=True,
        reload_data=True
    )



    # Get filtered data from visible rows
    filtered_df = grid_response['data']


    st.markdown(r"""
    ### Summary Highlights
    <details>
    <summary> Hot Jupiter around Hot Stars can have High Obliquity: 7σ</summary>
    <a href="https://ui.adsabs.harvard.edu/abs/2010ApJ...718L.145W/abstract" target="_blank">
        Winn, J. N., Fabrycky, D., Albrecht, S., et al. 2010, ApJL, 718, 2, L145.
    </a>
    <br/>
    <a href="https://ui.adsabs.harvard.edu/abs/2010ApJ...719..602S/abstract" target="_blank">
        Schlaufman, K. C. 2010, ApJ, 719, 1, 602.
    </a>
    </details>
    <details>
    <summary> Single Star Warm Jupiter tend to be aligned: 3.5σ</summary>
    <a href="https://ui.adsabs.harvard.edu/abs/2024ApJ...973L..21W/abstract" target="_blank">
        Wang, X.-Y., Rice, M., Wang, S., et al. 2024, ApJL, 973, 1, L21.
    </a>
    <br/>
    <a href="https://ui.adsabs.harvard.edu/abs/2022AJ....164..104R/abstract" target="_blank">
        Rice, M., Wang, S., Wang, X.-Y., et al. 2022, AJ,164, 3, 104.
    </a>
    </details>
    <br/><br/>
    Last updated: 2025/04/19
    """, unsafe_allow_html=True)

with col2:
    # st.subheader('Data Visualization')
    query_expr = st.text_area("**Data Visualization**: pandas.DataFrame.query() expression can be applied.", 
                              value="pl_projobliqabs_uerr < 50 and pl_projobliqabs_lerr < 50 and pl_projobliqabs < 900 and Pflag == 'y' and Binary== 0 and pl_bmassj > 0.3 and controversial ==0 and pl_bmassj_lerr > 0.0001", height=68)

    try:
        query_expr_single_line = " ".join(query_expr.strip().splitlines())
        plot_df = filtered_df.query(query_expr_single_line) if query_expr_single_line else filtered_df
    except Exception as e:
        st.error(f"Query error: {e}")
        plot_df = filtered_df

    if not plot_df.empty:
        numeric_columns = plot_df.select_dtypes(include='number').columns
        default_x = numeric_columns.get_loc('st_teff') if 'st_teff' in numeric_columns else 0
        default_y = numeric_columns.get_loc('pl_projobliqabs') if 'pl_projobliqabs' in numeric_columns else (1 if len(numeric_columns) > 1 else 0)

        x_axis = st.selectbox('Select X-axis', numeric_columns, index=default_x)
        y_axis = st.selectbox('Select Y-axis', numeric_columns, index=default_y)

        with st.expander("Advanced plot customization"):
            use_xerr = st.checkbox("Show X error bars", value=False)
            use_yerr = st.checkbox("Show Y error bars", value=False)
            marker_color = st.color_picker("Pick marker color", value="#ADD8E6")
            marker_symbol = st.selectbox("Select marker symbol", ["circle", "square", "diamond", "cross", "x", "triangle-up", "triangle-down"])
            marker_size = st.slider("Marker size", min_value=5, max_value=20, value=10)
            fig_title = st.text_input('Plot Title', value=f'{y_axis} vs {x_axis}')
            x_label = st.text_input('X-axis Label', value=pars2label.get(x_axis, x_axis))
            y_label = st.text_input('Y-axis Label', value=pars2label.get(y_axis, y_axis))

            custom_limits = st.checkbox("Manually set axis limits", value=False)

            if custom_limits:
                x_min = st.number_input("X-axis min", value=float(plot_df[x_axis].min()), step=0.1)
                x_max = st.number_input("X-axis max", value=float(plot_df[x_axis].max()), step=0.1)
                y_min = st.number_input("Y-axis min", value=float(plot_df[y_axis].min()), step=0.1)
                y_max = st.number_input("Y-axis max", value=float(plot_df[y_axis].max()), step=0.1)


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

        fig.update_layout(
            xaxis=dict(
                title=dict(text=x_label, font=dict(color='black')),
                autorange=not custom_limits,
                range=[x_min, x_max] if custom_limits else None,
                showline=True,
                showgrid=False,
                zeroline=False,
                visible=True
            ),
            yaxis=dict(
                title=dict(text=y_label, font=dict(color='black')),
                autorange=not custom_limits,
                range=[y_min, y_max] if custom_limits else None,
                showline=True,
                showgrid=False,
                zeroline=False,
                visible=True
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=60, r=60, t=60, b=60)
        )




        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for plotting.")
