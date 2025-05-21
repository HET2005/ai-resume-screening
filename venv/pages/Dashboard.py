import streamlit as st
import os
import json
import matplotlib.pyplot as plt

st.title("📈 Dashboard")


if not os.path.exists("results.json"):
    st.warning("No data available yet. Run Bulk Screening first.")
else:
    with open("results.json", "r") as f:
        data = json.load(f)

    ranked = data.get("ranked", [])
    skills = data.get("skills", {})

    st.subheader("🏆 Top Ranked Resumes")
    for i, (name, score) in enumerate(ranked[:5], 1):
        st.markdown(f"**{i}. {name}** — Score: `{score:.4f}`")

    st.subheader("🔥 Top Skills from All Resumes")
    if skills:
        skill_names = list(skills.keys())
        counts = list(skills.values())

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(skill_names, counts, color="#007FFF")
        ax.set_ylabel("Count")
        ax.set_title("Skill Frequency")
        st.pyplot(fig)
    else:
        st.info("No skills extracted.")
