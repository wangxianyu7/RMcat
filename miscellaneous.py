import streamlit as st
import numpy as np
import pandas as pd
st.title("Miscellaneous")

st.markdown("1) Estimate the maximum RM signal amplitude using an analytic approximation ([Albrecht+2022](https://ui.adsabs.harvard.edu/abs/2022PASP..134h2001A/abstract)):")

st.latex(r"""
RV_{\mathrm{RM(max)}} \approx 0.7 \sqrt{1 - b^2} \left( \frac{r}{R} \right)^2 v \sin i
""")



import streamlit as st
import pandas as pd
import numpy as np

# Load the CSV
df = pd.read_csv("vsini_ror_b.csv", usecols=[0, 1, 2, 3, 4], header=None)
df.columns = ['name',  'b','ror', 'vsini', 'ref_link']

# Provide an autocomplete-like dropdown
name_list = sorted(df['name'].dropna().unique())
target_name = st.selectbox("Select target name (autocomplete supported)", options=["<Manual Input>"] + name_list)



# Try to find the row
row = df[df['name'].str.lower() == target_name.lower()]

if not row.empty:
    vsini_val = float(row['vsini'].values[0]) if not pd.isna(row['vsini'].values[0]) else -999.0
    ror_val = float(row['ror'].values[0]) if not pd.isna(row['ror'].values[0]) else -999.0
    b_val = float(row['b'].values[0]) if not pd.isna(row['b'].values[0]) else -999.0
    ref_link = row['ref_link'].values[0]
    st.success(f"Target '{target_name}' found. Values loaded from table.")
    
    if pd.notna(ref_link) and ref_link.strip() != "":
        st.markdown(f"**Reference Link**: [source]({ref_link})")
    else:
        st.info("No reference link available for this target.")
else:
    vsini_val = ror_val = b_val = -999.0
    st.warning(f"Target '{target_name}' not found. Please input values manually.")

# Replace invalid placeholder values with NaN
vsini_display = vsini_val if vsini_val >= 0 else np.nan
ror_display = ror_val if ror_val >= 0 else np.nan
b_display = b_val if b_val >= 0 else np.nan

# Let user confirm or manually input values only if missing
if np.isnan(ror_display):
    pl_ror = st.number_input("Rp/Rs (not found, please enter manually)", min_value=0.0, step=0.01)
else:
    pl_ror = st.number_input("Rp/Rs", value=float(ror_display), min_value=0.0, step=0.01)

if np.isnan(vsini_display):
    vsini = st.number_input("Stellar vsini (km/s) (not found, please enter manually)", min_value=0.0, step=0.1)
else:
    vsini = st.number_input("Stellar vsini (km/s)", value=float(vsini_display), min_value=0.0, step=0.1)

if np.isnan(b_display):
    b = st.number_input("Impact parameter b (not found, please enter manually)", min_value=0.0, step=0.01)
else:
    b = st.number_input("Impact parameter b", value=float(b_display), min_value=0.0, step=0.01)

# Compute RM amplitude only if all values are provided
if all(val >= 0 for val in [pl_ror, vsini, b]) and b <= 1.0:
    RM_amp = 0.7 * pl_ror**2 * vsini * 1000 * np.sqrt(1 - b**2)
    st.write(f"Estimated RM Amplitude: **{RM_amp:.2f} m/s**")
else:
    st.info("Please provide valid values for all parameters to compute RM amplitude.")
