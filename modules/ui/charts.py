import altair as alt
import streamlit as st
from modules.palette import PAL_BLUE, PAL_ORANGE, PAL_TEAL

def draw(df):
    line_base = alt.Chart(df).encode(x="date:T")

    # Juice & Anxiety
    st.altair_chart(
        (line_base.mark_line(point=True, color=PAL_BLUE)
                 .encode(y="juice:Q")
       + line_base.mark_line(point=True, color=PAL_ORANGE)
                 .encode(y="anxiety:Q"))
        .properties(height=250),
        use_container_width=True
    )

    # GQ
    st.altair_chart(
        line_base.mark_line(point=True, color=PAL_TEAL)
                 .encode(y=alt.Y("gq:Q", title="GQ"))
                 .properties(height=200, title="Gumption Quotient"),
        use_container_width=True
    )

    # dGQ/dt bars
    st.altair_chart(
        (line_base.mark_bar(size=6)
                  .encode(y=alt.Y("dgqdt:Q", title="d GQ / d t"),
                          color=alt.condition("datum.dgqdt > 0",
                                              alt.value(PAL_TEAL),
                                              alt.value(PAL_ORANGE))))
        .properties(height=200, title="Daily change in GQ"),
        use_container_width=True
    )
