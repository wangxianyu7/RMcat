import streamlit as st
import numpy as np

st.title("Miscellaneous")

st.markdown("1) Estimate the maximum RM signal amplitude using an analytic approximation ([Albrecht+2022](https://ui.adsabs.harvard.edu/abs/2022PASP..134h2001A/abstract)):")

st.latex(r"""
RV_{\mathrm{RM(max)}} \approx 0.7 \sqrt{1 - b^2} \left( \frac{r}{R} \right)^2 v \sin i
""")


pl_ror = st.number_input("Rp/Rs", value=0.1, min_value=0.0, step=0.001)
vsini = st.number_input("Stellar vsini (km/s)", value=2.6, min_value=0.0, step=0.1)
b = st.number_input("Impact parameter b", value=0.1, min_value=0.0, max_value=1.0, step=0.01)
RM_amp = 0.7 * pl_ror**2 * vsini * 1000 * np.sqrt(1 - b**2)

st.write(f"Estimated RM Amplitude: {RM_amp:.2f} m/s")
