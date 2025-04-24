import streamlit as st

st.markdown("# True Obliquity (ψ) calculator 🪐")
st.sidebar.markdown("# True Obliquity (ψ) calculator 🪐")


import streamlit as st
import coPsi
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import skewnorm
import warnings
import pandas as pd
import os
warnings.filterwarnings("ignore", category=UserWarning, append=True)

# Skewed normal fitting

def calculate_skewed_normal_params(median, lower_err, upper_err):
    lower_err = np.abs(lower_err)
    upper_err = np.abs(upper_err)
    reference = np.array([(median - lower_err), median, (median + upper_err)])

    def fake_lnlike(p):
        alpha, loc, scale = p
        ppf = skewnorm.ppf([0.15865, 0.5, 0.84135], alpha, loc=loc, scale=scale)
        fake_lnlike = np.sum((ppf - reference) ** 2)
        return np.inf if np.isnan(fake_lnlike) else fake_lnlike

    loc_guess = median
    scale_guess = np.mean([lower_err, upper_err])
    sol = None
    for alpha_guess in [-10, -1, 0, 1, 10]:
        initial_guess = (alpha_guess, loc_guess, scale_guess)
        sol1 = minimize(fake_lnlike, initial_guess, bounds=[(None, None), (None, None), (0, None)])
        if sol is None or sol1.fun < sol.fun:
            sol = sol1
    return sol.x

def simulate_PDF(median, lower_err, upper_err, size=1):
    alpha, loc, scale = calculate_skewed_normal_params(median, lower_err, upper_err)
    return skewnorm.rvs(alpha, loc=loc, scale=scale, size=size)


st.header("Input Parameters")
N = st.number_input("Number of Samples", min_value=1000, value=10000, step=1000)

# Input values
Rs_mu = st.number_input("Rs Median (Rsun)", value=1.47)
Rs_sigma = st.number_input("Rs Sigma (Rsun)", value=0.017)
Rs_lower_bound = st.number_input("Rs Lower Bound (Rsun)", value=0.5)
Rs_upper_bound = st.number_input("Rs Upper Bound (Rsun)", value=2.0)
Rs_type = st.selectbox("Rs Distribution Type", options=['gauss','tgauss','uniform','jeff'], index=0)

Prot_mu = st.number_input("Prot Median (days)", value=9.77)
Prot_sigma = st.number_input("Prot Sigma (days)", value=0.98)
Prot_lower_bound = st.number_input("Prot Lower Bound (days)", value=0.5)
Prot_upper_bound = st.number_input("Prot Upper Bound (days)", value=22.0)
Prot_type = st.selectbox("Prot Distribution Type", options=['gauss','tgauss','uniform','jeff'], index=0)

vsini_mu = st.number_input("Vsini Median (km/s)", value=7)
vsini_sigma = st.number_input("Vsini Sigma (km/s)", value=1.1)
vsini_lower_bound = st.number_input("Vsini Lower Bound (km/s)", value=1.0)
vsini_upper_bound = st.number_input("Vsini Upper Bound (km/s)", value=12.0)
vsini_type = st.selectbox("Vsini Distribution Type", options=['gauss','tgauss','uniform','jeff'], index=0)

lam = st.number_input("Lambda Median (deg)", value=6)
lam_lerr = st.number_input("Lambda Lower Error (deg)", value=16)
lam_uerr = st.number_input("Lambda Upper Error (deg)", value=17)
pl_orbinc = st.number_input("Orbital Inclination Median (deg)", value=88.3)
pl_orbinc_lerr = st.number_input("Orbital Inclination Lower Error (deg)", value=0.36)
pl_orbinc_uerr = st.number_input("Orbital Inclination Upper Error (deg)", value=0.56)

import io
import contextlib

terminal_output = st.empty()

if st.button("Run Inclination Analysis"):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        incs = coPsi.iStar(
        Rs=(Rs_mu, Rs_sigma, Rs_lower_bound, Rs_upper_bound, Rs_type),
        Prot=(Prot_mu, Prot_sigma, Prot_lower_bound, Prot_upper_bound, Prot_type),
        vsini=(vsini_mu, vsini_sigma, vsini_lower_bound, vsini_upper_bound, vsini_type)
    )

    res_df = incs.stellarInclination(plot_convergence=False, plot_corner=False, plot_vsini=False)
    terminal_output.text(buffer.getvalue())
    st.success(f"Stellar inclination: {res_df['incs'][0]:.2f} +{res_df['incs'][2]:.2f} -{res_df['incs'][1]:.2f}")
    st.success(f"Latex format: i_* = {res_df['incs'][0]:.2f}^{{+{res_df['incs'][2]:.2f}}}_{{-{res_df['incs'][1]:.2f}}}")

    incs.createDistributions()
    incs.dist['incs'] = simulate_PDF(res_df['incs'][0], res_df['incs'][1], res_df['incs'][2], size=N)
    incs.dist['lam'] = simulate_PDF(lam, lam_lerr, lam_uerr, size=N)
    incs.dist['inco'] = simulate_PDF(pl_orbinc, pl_orbinc_lerr, pl_orbinc_uerr, size=N)

    incs.coPsi()
    # incs.diagnostics('cosp')
    # incs.savePosterior(post='cosp', name='cospi')
    # incs.savePosterior(post='incs', name='incs')
    psi_dist = incs.dist['psi']
    incs_dist = incs.dist['incs']
    
    psi_v, psi_u, psi_l = incs.getConfidence(psi_dist)
    incs_v, incs_u, incs_l = incs.getConfidence(incs_dist)
    np.savetxt("psi.csv", psi_dist, delimiter=",", header="psi")
    np.savetxt("incs.csv", incs_dist, delimiter=",", header="incs")
    
    if os.path.exists("incs.csv"):
        df_incs = pd.read_csv("incs.csv")
        
        # Calculate and show psi statistics
        incs_deg = df_incs['# incs']
        z = incs_deg
        
        val, up, low = incs.getConfidence(z,lev=0.68)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        xkde, ykde = incs.getKDE(z)
        ax.plot(xkde,ykde,color='k')

        vals = (xkde > (val-low)) & (xkde < (up+val))
        xs = xkde[vals]
        ys = ykde[vals]
        ax.fill_between(xs,ys,color='C0',alpha=0.5, label=r"$\rm HPD$")


        ax.set_ylim(ymin=0.0)
        ax.set_xlim(np.min(xkde),np.max(xkde))

        ax.set_ylabel(r'$\rm KDE$')
        ax.set_xlabel(r'$\rm i_*$ (degrees)')

        idx = np.argmin(abs(xkde-val))
        plt.vlines(val,ymin=0,ymax=ykde[idx],linestyle='-',color='k')
        idx_up = np.argmin(abs(xkde-(up+val)))
        plt.vlines(up+val,ymin=0,ymax=ykde[idx_up],linestyle='--',color='k')
        idx_low = np.argmin(abs(xkde-(val-low)))
        plt.vlines(val-low,ymin=0,ymax=ykde[idx_low],linestyle='--',color='k')
        st.pyplot(fig)
        
        
        
        # st.subheader("incs.csv")
        # st.dataframe(df_incs)
        st.download_button("Download incs.csv", data=df_incs.to_csv(index=False), file_name="incs.csv")


    # Show and download posterior CSV files
    if os.path.exists("cospi.csv"):
        st.success(f"True Obliquity: {psi_v:.2f} +{psi_u:.2f} -{psi_l:.2f}")
        st.success(f"Latex format: \psi = {psi_v:.2f}^{{+{psi_u:.2f}}}_{{-{psi_l:.2f}}}")
        df_cospi = pd.read_csv("psi.csv")
        
        # Calculate and show psi statistics
        incs_deg = df_cospi['# psi']
        z = incs_deg
        
        val, up, low = incs.getConfidence(z,lev=0.68)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        xkde, ykde = incs.getKDE(z)
        ax.plot(xkde,ykde,color='k')

        vals = (xkde > (val-low)) & (xkde < (up+val))
        xs = xkde[vals]
        ys = ykde[vals]
        ax.fill_between(xs,ys,color='C0',alpha=0.5, label=r"$\rm HPD$")


        ax.set_ylim(ymin=0.0)
        ax.set_xlim(np.min(xkde),np.max(xkde))

        ax.set_ylabel(r'$\rm KDE$')
        ax.set_xlabel(r'$\rm \psi$ (degrees)')

        idx = np.argmin(abs(xkde-val))
        plt.vlines(val,ymin=0,ymax=ykde[idx],linestyle='-',color='k')
        idx_up = np.argmin(abs(xkde-(up+val)))
        plt.vlines(up+val,ymin=0,ymax=ykde[idx_up],linestyle='--',color='k')
        idx_low = np.argmin(abs(xkde-(val-low)))
        plt.vlines(val-low,ymin=0,ymax=ykde[idx_low],linestyle='--',color='k')
        st.pyplot(fig)
        

        # st.subheader("cospi.csv")
        st.download_button("Download cospi.csv", data=df_cospi.to_csv(index=False), file_name="cospi.csv")