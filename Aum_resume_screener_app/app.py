import streamlit as st
import pandas as pd
import numpy as np
from utils import (
    load_model,
    extract_text_from_file,
    preprocess_text,
    get_embeddings,
    calculate_cosine_similarity,
)

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="ResuStreamPro")

# --- Initialize Session State ---
if "resumes_data" not in st.session_state:
    st.session_state.resumes_data = []  # List to store {filename, raw_text, processed_text, embedding}
if "selected_model_name" not in st.session_state:
    st.session_state.selected_model_name = "all-MiniLM-L6-v2"  # Default model
if "matching_threshold" not in st.session_state:
    st.session_state.matching_threshold = 0.70
if "model" not in st.session_state:
    st.session_state.model = load_model(st.session_state.selected_model_name)
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- Sidebar ---
with st.sidebar:
    st.title("ResuStreamPro")

    page_options = ["Home", "Upload", "Dashboard", "Settings", "Benchmark"]
    st.session_state.current_page = st.radio(
        "Navigation",
        page_options,
        index=page_options.index(st.session_state.current_page),
    )

    st.markdown("---")
    st.header("Global Settings")

    # AI Model Selection
    model_options = [
        "all-MiniLM-L6-v2",
        "paraphrase-MiniLM-L6-v2",
        "multi-qa-MiniLM-L6-cos-v1",
    ]
    new_model_name = st.selectbox(
        "Select AI Model",
        options=model_options,
        index=model_options.index(st.session_state.selected_model_name),
    )
    if new_model_name != st.session_state.selected_model_name:
        st.session_state.selected_model_name = new_model_name
        with st.spinner(f"Loading model: {st.session_state.selected_model_name}..."):
            st.session_state.model = load_model(st.session_state.selected_model_name)
        st.success(f"Model '{st.session_state.selected_model_name}' loaded.")
        st.rerun()  # Rerun to reflect model change immediately

    # Matching Threshold
    st.session_state.matching_threshold = st.slider(
        "Matching Threshold", 0.0, 1.0, st.session_state.matching_threshold, 0.01
    )

# --- Main Page Content ---

# Home Page
if st.session_state.current_page == "Home":
    st.header("Welcome to ResuStreamPro")
    st.markdown("""
    An AI-Powered Resume Screening System to streamline your hiring process.
    Navigate through the pages using the sidebar to upload resumes, view dashboards, or adjust settings.
    """)
    if st.session_state.model is None:
        st.error(
            "The AI model could not be loaded. Please check the model selection or try again."
        )
    else:
        st.info(f"Currently using AI model: **{st.session_state.selected_model_name}**")

# Upload Page
elif st.session_state.current_page == "Upload":
    st.header("Upload Resumes")

    uploaded_files = st.file_uploader(
        "Drag and drop files here or click to browse",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Limit 200MB per file • PDF, DOCX, TXT",
    )

    if uploaded_files:
        newly_uploaded_filenames = [f.name for f in uploaded_files]
        existing_filenames = [r["filename"] for r in st.session_state.resumes_data]

        processed_count = 0
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in existing_filenames:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    raw_text = extract_text_from_file(uploaded_file)
                    if raw_text and raw_text.strip():
                        processed_text = preprocess_text(raw_text)
                        embedding = get_embeddings(
                            processed_text, st.session_state.model
                        )
                        if embedding is not None:
                            st.session_state.resumes_data.append(
                                {
                                    "filename": uploaded_file.name,
                                    "raw_text": raw_text,
                                    "processed_text": processed_text,
                                    "embedding": embedding.cpu(),  # Store on CPU
                                }
                            )
                            processed_count += 1
                        else:
                            st.warning(
                                f"Could not generate embedding for {uploaded_file.name}. Skipping."
                            )
                    else:
                        st.warning(
                            f"No text extracted or empty content in {uploaded_file.name}. Skipping."
                        )
            else:
                st.info(
                    f"Resume '{uploaded_file.name}' has already been uploaded and processed."
                )

        if processed_count > 0:
            st.success(
                f"Successfully processed and embedded {processed_count} new resume(s)."
            )

    st.subheader("Uploaded Resumes")
    if not st.session_state.resumes_data:
        st.info("No resumes uploaded yet.")
    else:
        filenames = [resume["filename"] for resume in st.session_state.resumes_data]
        df_resumes = pd.DataFrame({"Uploaded Resume Filenames": filenames})
        st.dataframe(df_resumes, use_container_width=True)

        if st.button("Clear All Uploaded Resumes"):
            st.session_state.resumes_data = []
            st.success("All uploaded resumes have been cleared.")
            st.rerun()


# Dashboard Page
elif st.session_state.current_page == "Dashboard":
    st.header("Candidate Dashboard")

    if not st.session_state.resumes_data:
        st.warning("Please upload resumes first on the 'Upload' page.")
    else:
        job_description = st.text_area(
            "Enter Job Description", height=200, key="jd_input"
        )

        if st.button("Match Candidates", type="primary"):
            if not job_description.strip():
                st.error("Please enter a job description.")
            elif st.session_state.model is None:
                st.error(
                    "AI model not loaded. Please select a model in Global Settings."
                )
            else:
                with st.spinner(
                    "Processing job description and matching candidates..."
                ):
                    processed_jd = preprocess_text(job_description)
                    jd_embedding = get_embeddings(processed_jd, st.session_state.model)

                    if jd_embedding is not None:
                        results = []
                        for resume_data in st.session_state.resumes_data:
                            if resume_data["embedding"] is not None:
                                similarity_score = calculate_cosine_similarity(
                                    jd_embedding.cpu(),  # Ensure JD embedding is on CPU for comparison
                                    resume_data[
                                        "embedding"
                                    ].cpu(),  # Ensure resume embedding is on CPU
                                )
                                results.append(
                                    {
                                        "Filename": resume_data["filename"],
                                        "Similarity Score": float(
                                            similarity_score[0][0]
                                        ),
                                        "Processed Text": resume_data[
                                            "processed_text"
                                        ],  # For display/debug
                                    }
                                )
                            else:
                                results.append(
                                    {
                                        "Filename": resume_data["filename"],
                                        "Similarity Score": 0.0,  # Or some indicator of error
                                        "Processed Text": "Error: Embedding not available",
                                    }
                                )

                        ranked_results = sorted(
                            results, key=lambda x: x["Similarity Score"], reverse=True
                        )

                        # Filter by threshold
                        filtered_results = [
                            res
                            for res in ranked_results
                            if res["Similarity Score"]
                            >= st.session_state.matching_threshold
                        ]

                        st.subheader("Matching Results")
                        if not filtered_results:
                            st.info(
                                f"No candidates found matching the threshold of {st.session_state.matching_threshold:.2f}."
                            )
                            if (
                                ranked_results
                            ):  # Show top results even if below threshold, if any
                                st.write("Top results (below threshold):")
                                df_top_results = pd.DataFrame(ranked_results[:5])
                                st.dataframe(
                                    df_top_results[["Filename", "Similarity Score"]],
                                    use_container_width=True,
                                )
                        else:
                            df_results = pd.DataFrame(filtered_results)
                            st.dataframe(
                                df_results[["Filename", "Similarity Score"]],
                                use_container_width=True,
                            )

                            st.subheader("Candidate Details")
                            for res in filtered_results:
                                with st.expander(
                                    f"{res['Filename']} (Score: {res['Similarity Score']:.3f})"
                                ):
                                    st.text_area(
                                        "Processed Resume Text Snippet:",
                                        value=res["Processed Text"][:1000] + "...",
                                        height=150,
                                        disabled=True,
                                        key=f"details_{res['Filename']}",
                                    )
                    else:
                        st.error("Could not process the job description.")

        st.markdown("---")
        st.caption(
            "Enter a job description and click 'Match Candidates' to see results based on the uploaded resumes."
        )


# Settings Page
elif st.session_state.current_page == "Settings":
    st.header("Settings")

    st.write(
        "Adjust global application settings here. Changes made in the sidebar are reflected here and vice-versa."
    )

    # Matching Threshold (can be duplicated here for convenience or this page can host other settings)
    st.session_state.matching_threshold = st.slider(
        "Matching Threshold (synced with sidebar)",
        0.0,
        1.0,
        st.session_state.matching_threshold,
        0.01,
        key="settings_threshold_slider",  # Unique key if same component used multiple times
    )
    st.info(f"Current matching threshold: {st.session_state.matching_threshold:.2f}")

    st.markdown("---")
    st.subheader("Cache Management")
    if st.button("Clear Model Cache"):
        load_model.clear()  # Clears the cache for the model loading function
        st.session_state.model = None  # Force reload on next access
        st.success(
            "AI Model cache cleared. The model will be re-downloaded on next use if needed."
        )
        st.info(
            "You might need to re-select the model or navigate to trigger a reload."
        )

    st.markdown("---")
    st.write("Other application settings can be added here in the future.")
    # Example: Enable Caching (conceptual)
    enable_caching = st.toggle("Enable Advanced Caching (Future Feature)", value=True)
    if enable_caching:
        st.write("Advanced caching is ON.")
    else:
        st.write("Advanced caching is OFF.")

# --- Benchmark Page ---
if "benchmark_results" not in st.session_state:
    try:
        st.session_state.benchmark_results = pd.read_csv("benchmark_results.csv")
    except Exception:
        st.session_state.benchmark_results = None

if st.session_state.current_page == "Benchmark":
    st.header("Benchmark Results")
    results_df = st.session_state.benchmark_results
    if results_df is None:
        st.warning("No benchmark results found. Please run the benchmark script first.")
    else:
        import matplotlib.pyplot as plt
        import seaborn as sns

        st.markdown("### Distribution of Top Resume Similarity Scores by Model")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="model", y="top_resume_score", data=results_df)
        plt.title("Distribution of Top Resume Similarity Scores by Model")
        plt.ylabel("Top Resume Similarity Score")
        plt.xlabel("Model")
        st.pyplot(plt.gcf())
        plt.clf()

        st.markdown("### Average Top Resume Similarity Score by Model")
        avg_scores = (
            results_df.groupby("model")["top_resume_score"].mean().reset_index()
        )
        plt.figure(figsize=(8, 5))
        sns.barplot(x="model", y="top_resume_score", data=avg_scores)
        plt.title("Average Top Resume Similarity Score by Model")
        plt.ylabel("Average Top Similarity Score")
        plt.xlabel("Model")
        st.pyplot(plt.gcf())
        plt.clf()

        st.markdown("---")
        st.dataframe(results_df, use_container_width=True)
