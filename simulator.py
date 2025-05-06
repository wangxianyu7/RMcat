import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from astropy.time import Time
import ironman
import matplotlib.gridspec as gridspec

st.set_page_config(layout="wide")
st.title("RM Simulator 🪐")

st.markdown("Powered by [ironman+Hirano2010](https://github.com/jiespinozar/ironman).")
st.markdown("⚠️ λ uncertainty estimation is not supported here due to limited compute. Full code is available [here](https://github.com/jiespinozar/ironman/blob/main/Examples/2%20-%20Example%20Simulating%20data.ipynb).")
st.markdown("### Enter Transit Window")
start_time = st.text_input("Start Time (UTC)", value="2022-12-27T03:00:00")
end_time = st.text_input("End Time (UTC)", value="2022-12-27T09:00:00")

st.markdown("### Enter System Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    per_p1 = st.number_input("Orbital Period [days]", value=18.09537)
    t0_p1 = st.number_input("Mid-Transit Time (BJD)", value=2458529.32785)
    aRs_p1 = st.number_input("a/R*", value=19.01)
    inc_p1 = st.number_input("Inclination [deg]", value=84.25)
    p_p1 = st.number_input("Rp/Rs", value=0.069)

with col2:
    rv_prec = st.number_input("RV Precision [m/s]", value=10.0)
    exp_time = st.number_input("Exposure Time [s]", value=300)
    e_p1 = st.number_input("Eccentricity", value=0.72)
    omega_p1 = st.number_input("ω [deg]", value=60.5)
    teff_star = st.number_input("Teff [K]", value=6800.0)

with col3:
    R_spec = st.number_input("Spectral Resolution", value=140000.0)
    lam_p1 = st.number_input("λ [deg]", value=1.2)
    vsini_star = st.number_input("v sin(i) [km/s]", value=20.2)
    u1 = st.number_input("Limb Darkening u1", value=0.32694400)
    u2 = st.number_input("Limb Darkening u2", value=0.33127792)

simulate = st.button("Simulate RM Observation")

if simulate:
    try:
        tr_window = Time([start_time, end_time], format='isot', scale='utc').jd
    except Exception as e:
        st.error(f"Invalid date format: {e}")
        st.stop()

    # Define system dictionary
    dct_system = {
        "per_p1": per_p1,
        "aRs_p1": aRs_p1,
        "inc_p1": inc_p1,
        "vsini_star": vsini_star,
        "p_p1": p_p1,
        "rv_prec": rv_prec,
        "exp_time": exp_time,
        "e_p1": e_p1,
        "omega_p1": omega_p1,
        "teff_star": teff_star,
        "R_spec": R_spec,
        "lam_p1": lam_p1,
        "t0_p1": t0_p1,
        "u": [u1, u2]
    }

    # Simulate observation times
    bjd_obs = np.arange(tr_window[0], tr_window[1], exp_time / 86400.0)

    # Simulate observed data
    sim_data_obs, error_obs = ironman.create_RM_data(bjd_obs, dct_system)

    # Convert to hours from mid-transit
    epoch = np.round((bjd_obs[0] - t0_p1) / per_p1)
    bjd_hr_obs = (bjd_obs - t0_p1 - epoch * per_p1) * 24.0

    # Simulate noise-free model
    dct_system["rv_prec"] = 0
    bjd_model = np.arange(tr_window[0]-1, tr_window[1]+1, 1 / (60 * 24.0))
    sim_data_model, _ = ironman.create_RM_data(bjd_model, dct_system)
    epoch_model = np.round((bjd_model[0] - t0_p1) / per_p1)
    bjd_hr_model = (bjd_model - t0_p1 - epoch_model * per_p1) * 24.0

    # Plotting
    fig = plt.figure(figsize=(6, 5), dpi=150)
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0,hspace=0)
    # hspace=0.0, vspace=0.0
    ax = plt.subplot(gs[0])



    eline_cap_lw = 1
    capsize = 2
    ax.errorbar(bjd_hr_obs, sim_data_obs, yerr=error_obs, fmt=".",  color="silver", elinewidth=eline_cap_lw, capthick=eline_cap_lw, capsize=capsize)
    ax.scatter(bjd_hr_obs, sim_data_obs, color="lightblue", s=20, label="Simulated RV", zorder=100, edgecolor="k")
    ax.plot(bjd_hr_model, sim_data_model, label="Model", color="firebrick", ls="--")
    ax.set_ylabel("RV (m/s)")
    ax.set_xticklabels([])
    xlim = np.max([abs(np.min(bjd_hr_obs)), abs(np.max(bjd_hr_obs))])
    ax.set_xlim(-xlim, xlim)
    ax.legend()

    # Optional: residuals or empty second subplot
    ax2 = plt.subplot(gs[1])
    residuals = sim_data_obs - np.interp(bjd_hr_obs, bjd_hr_model, sim_data_model)
    ax2.errorbar(bjd_hr_obs, residuals, error_obs, fmt=".", color="silver", elinewidth=eline_cap_lw, capthick=eline_cap_lw, capsize=capsize)
    ax2.scatter(bjd_hr_obs, residuals, color="lightblue", s=20, label="Residuals", zorder=100, edgecolor="k")
    ax2.axhline(0.0, color="firebrick", linestyle="--")
    ax2.set_ylabel("Residuals (m/s)")
    ylim_uerr, ylim_lerr = ax2.get_ylim()
    ylim = np.max([abs(ylim_uerr), abs(ylim_lerr)])
    ax2.set_ylim(-ylim, ylim)
    ax2.set_xlabel("Hours from Mid-Transit")
    ax2.set_xlim(-xlim, xlim)

    for ax_ in [ax,ax2]:
        ax_.tick_params(direction='in', which='both',  colors='k', bottom='True',top='True', left='True', right='True')
    
    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Download Plot", data=buf.getvalue(), file_name="rm_simulation.png", mime="image/png")
