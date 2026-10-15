import streamlit as st
import pandas as pd
from analyze import analyze, DATA, ANOMALY_THRESHOLD_PCT

st.set_page_config(page_title="FreightTiger Cost Watch", page_icon="🚚", layout="wide")
st.title("🚚 FreightTiger | Shipping Cost Watch")
st.caption("Deterministic weekly cost monitoring with evidence-grounded context matching.")
try:
    df = analyze()
except Exception as exc:
    st.error(f"Could not process the supplied data: {exc}")
    st.stop()

c1,c2,c3,c4=st.columns(4)
c1.metric("Route-weeks analyzed", f"{len(df):,}")
c2.metric("Unexplained flags", f"{(df.flagged=='Yes').sum():,}")
c3.metric("Justified increases", f"{(df.flagged=='No (justified)').sum():,}")
c4.metric("Threshold", f"+{ANOMALY_THRESHOLD_PCT:.0f}%")
routes=sorted(df.route.unique())
selected=st.multiselect("Filter routes",routes,default=routes)
status=st.multiselect("Verdict",df.flagged.unique().tolist(),default=df.flagged.unique().tolist())
view=df[df.route.isin(selected) & df.flagged.isin(status)].copy()
st.subheader("Findings")
st.dataframe(view, use_container_width=True, hide_index=True)
st.download_button("Download filtered findings CSV",view.to_csv(index=False).encode("utf-8"),"freight_cost_findings.csv","text/csv")
st.subheader("Route cost trend")
if selected:
    trend=df[df.route.isin(selected)].copy()
    trend["week_of"]=pd.to_datetime(trend["week_of"])
    chart=trend.pivot_table(index="week_of",columns="route",values="cost_per_tonne_km",aggfunc="mean")
    st.line_chart(chart)
st.info("A 'Yes' verdict means the increase crosses the documented threshold and no valid supplied note supports it. 'No (justified)' means an applicable note supports the flagged increase. The numerical pipeline does not call an LLM, so values and verdicts are reproducible.")
