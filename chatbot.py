import streamlit as st
from streamlit.components.v1 import html   # alias for convenience
from streamlit.components.v1 import iframe   # ← simpler alias
# ------------------------------------------------
# Page-level settings
# ------------------------------------------------
# st.set_page_config(
#     page_title="Stellar Obliquity Chatbot",
#     page_icon="🤖",
#     layout="wide",
# )

st.markdown("# Stellar Obliquity Chatbot 🤖")
st.sidebar.markdown("## Stellar Obliquity Chatbot 🤖")
# ------------------------------------------------
# Embed the CoBundle page
# ------------------------------------------------
iframe(
    src="https://www.cobundle.ai/s/JjqdFoV8yL/stellar_obliquity/",
    height=1200,          # px; make taller if you like
    scrolling=True,      # show a scrollbar when needed
)
# ------------------------------------------------
# Simple fixed-height <iframe>
# ------------------------------------------------
# html(
#     """
#     <iframe
#         src="https://www.cobundle.ai/s/JjqdFoV8yL/stellar_obliquity/"
#         style="width:100%;height:100vh;border:0;border-radius:8px;overflow:hidden;"
#         loading="lazy"
#         allow="clipboard-read; clipboard-write; encrypted-media">
#     </iframe>
#     """,
#     height=1000,   # fallback for browsers that ignore 100 vh inside iframes
# )

# # ------------------------------------------------
# # 100 % responsive (uncomment if preferred)
# # ------------------------------------------------
# html(
#     '''
#     <style>
#     .embed-container{
#       position:relative;
#       padding-top:56.25%;   /* 16 : 9 aspect ratio; tweak as desired */
#       height:0;overflow:hidden;
#     }
#     .embed-container iframe{
#       position:absolute;top:0;left:0;
#       width:100%;height:100%;
#       border:0;border-radius:8px;
#     }
#     </style>
#     <div class="embed-container">
#       <iframe
#           src="https://www.cobundle.ai/s/JjqdFoV8yL/stellar_obliquity/"
#           loading="lazy"
#           allow="clipboard-read; clipboard-write; encrypted-media">
#       </iframe>
#     </div>
#     ''',
#     height=0   # Streamlit ignores height when 0, letting CSS drive size
# )
