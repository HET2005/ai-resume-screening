import json
import os
import streamlit as st

JD_FILE_PATH = "jd_library.json"

def load_jds():
    try:
        if not os.path.exists(JD_FILE_PATH):
            st.warning(f"JD file not found at path: {JD_FILE_PATH}")
            return []
        with open(JD_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        st.error(f"Error loading JD library JSON: {e}")
        return []

def save_jds(data):
    try:
        with open(JD_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving JD library JSON: {e}")

def add_jd(title, description):
    jds = load_jds()
    max_id = max([int(jd["id"]) for jd in jds], default=0)
    new_id = str(max_id + 1)
    jds.append({"id": new_id, "title": title, "description": description})
    save_jds(jds)

def update_jd(jd_id, title, description):
    jds = load_jds()
    for jd in jds:
        if jd["id"] == jd_id:
            jd["title"] = title
            jd["description"] = description
            break
    save_jds(jds)

def delete_jd(jd_id):
    jds = load_jds()
    jds = [jd for jd in jds if jd["id"] != jd_id]
    save_jds(jds)
