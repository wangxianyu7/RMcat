import streamlit as st

st.markdown("# Modeling softwares 🛠️")
st.sidebar.markdown("# Modeling softwares 🛠️")


st.markdown("""This page contains a list of modeling softwares that can be used to model the RM effect. The list is not exhaustive and is meant to give an overview of the available options. If you have any suggestions for additions, please let us know!""")
st.markdown("### RM models and modeling Tools")
st.markdown("[Ohta et al.(2005)](https://ui.adsabs.harvard.edu/abs/2005ApJ...622.1118O/abstract), [Hirano et al.(2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...709..458H/abstract), [Hirano et al.(2011)](https://ui.adsabs.harvard.edu/abs/2011ApJ...742...69H/abstract), [Boue et al.(2013)](https://ui.adsabs.harvard.edu/abs/2013A%26A...550A..53B/abstract), [Covino et al.(2013)](https://ui.adsabs.harvard.edu/abs/2013A%26A...554A..28C/abstract), [Cegla et al.(2016)](https://ui.adsabs.harvard.edu/abs/2016A%26A...588A.127C/abstract), [Bourrier et al.(2021)](https://ui.adsabs.harvard.edu/abs/2021A%26A...654A.152B/abstract)")


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Ohta2005")
    st.markdown("#### [Allesfitter + ellc](https://github.com/MNGuenther/allesfitter) ")
    st.markdown("#### [EXOFASTv2 + Ohta2005](https://github.com/jdeast/EXOFASTv2)")
    st.markdown("#### [Exoplanet](https://github.com/exoplanet-dev/exoplanet) + [Starry](https://github.com/rodluger/starry)")
    

with col2:
    st.markdown("### Hirano2011")
    
    st.markdown("#### [tracit](https://github.com/emilknudstrup/tracit)")
    st.markdown("#### [Allesfitter + Hirano2011](https://github.com/wangxianyu7/Allesfitters)")
    st.markdown("#### [EXOFASTv2 + Hirano2011](https://github.com/wangxianyu7/EXOFASTv2)")
    

with col3:
    st.markdown("#### [Ironman](https://github.com/jiespinozar/ironman) & [rmfit](https://github.com/gummiks/rmfit) (Hirano2010)")
    st.markdown("#### [PyAORME](https://github.com/andres-jordan/PyARoME) (Boue2013)")
    st.markdown("#### [PyORBIT](https://github.com/LucaMalavolta/PyORBIT) (Covino2013)")

st.markdown("### The Rossiter–McLaughlin effect revolutions pipeline")
st.markdown("#### [ANTARESS](https://gitlab.unige.ch/spice_dune/antaress) (Bourrier2021)")