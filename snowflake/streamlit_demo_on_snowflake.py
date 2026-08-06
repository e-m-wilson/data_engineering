# Import python packages
import streamlit as st
import os

# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")

st.write("""
Replace this example with your own code!
""")

st.markdown("""
- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
""")

# ---------------- Sidebar ----------------
st.sidebar.header("Controls")

hifives_val = st.sidebar.slider(
    "Number of high-fives in Q3",
    min_value=0,
    max_value=90,
    value=60,
    help="Use this to enter the number of high-fives you gave in Q3",
)

# Create a database connection to Snowflake
conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = conn.session()

# Create an example dataframe
created_dataframe = session.create_dataframe(
    [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
    schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
)

queried_data = created_dataframe.to_pandas()

# ---------------- Metrics ----------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total High-Fives",
    queried_data["HIGH_FIVES"].sum()
)

col2.metric(
    "Q3 High-Fives",
    hifives_val
)

col3.metric(
    "Total Fist Bumps",
    queried_data["FIST_BUMPS"].sum()
)

# ---------------- Chart ----------------
st.subheader("High-Fives by Quarter")
st.bar_chart(
    queried_data,
    x="QUARTER",
    y="HIGH_FIVES"
)

# ---------------- Dataframe ----------------
st.subheader("Underlying Data")
st.dataframe(queried_data, use_container_width=True)