import streamlit as st
import os
import json
import pandas as pd
import altair as alt

st.set_page_config(page_title="Resume Screening Dashboard", page_icon="📊", layout="wide")

st.title("📈 Resume Screening Dashboard")

if not os.path.exists("results.json"):
    st.warning("No data available yet. Run Bulk Screening first.")
else:
    with open("results.json", "r") as f:
        data = json.load(f)

    ranked = data.get("ranked", [])
    skills = data.get("skills", {})

    total_resumes = len(ranked)
    st.markdown(f"### 🗂️ Total Resumes Processed: **{total_resumes}**")

    # Sidebar controls
    st.sidebar.header("Settings")
    top_n = st.sidebar.slider("Show Top N Resumes", min_value=1, max_value=20, value=5)
    skill_filter = st.sidebar.text_input("Filter Skills by Name (case-insensitive)")

    # Top Ranked Resumes Section
    with st.expander("🏆 Top Ranked Resumes", expanded=True):
        if ranked:
            for i, (name, score) in enumerate(ranked[:top_n], 1):
                st.markdown(f"**{i}. {name}** — Similarity Score: `{score:.4f}`")
        else:
            st.info("No ranked resumes found.")

    # Skills Section
    with st.expander("🔥 Top Skills from All Resumes", expanded=True):
        if skills:
            # Filter and sort skills
            filtered_skills = {k: v for k, v in skills.items() if skill_filter.lower() in k.lower()}
            if not filtered_skills:
                st.info("No skills match your filter.")
            else:
                sorted_skills = sorted(filtered_skills.items(), key=lambda x: x[1], reverse=True)
                df_skills = pd.DataFrame(sorted_skills, columns=["Skill", "Count"])
                df_skills["Percent"] = (df_skills["Count"] / df_skills["Count"].sum()) * 100

                # Altair horizontal bar chart with percentages
                chart = (
                    alt.Chart(df_skills)
                    .mark_bar(color="#007FFF")
                    .encode(
                        x=alt.X("Count:Q", title="Count"),
                        y=alt.Y("Skill:N", sort='-x', title="Skill"),
                        tooltip=["Skill", "Count", alt.Tooltip("Percent", format=".2f")]
                    )
                )

                text = chart.mark_text(
                    align='left',
                    baseline='middle',
                    dx=3  # Nudges text to right so it doesn't overlap bars
                ).encode(text=alt.Text("Percent", format=".2f"))

                st.altair_chart(chart + text, use_container_width=True)
        else:
            st.info("No skills extracted.")
