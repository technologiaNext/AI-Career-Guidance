import streamlit as st
import json
import os

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Career Guidance Agent",
    layout="wide"
)

# =========================================================
# LOAD JSON DATA
# =========================================================

json_file = "career_paths.json"

# Create file if not exists
if not os.path.exists(json_file):

    with open(json_file, "w") as f:
        json.dump({}, f)

# Load data
with open(json_file, "r") as f:
    career_data = json.load(f)

# =========================================================
# TITLE
# =========================================================


# =========================================================
# TITLE + LIKE COUNTER
# =========================================================

likes_file = "likes.json"

# Create file if not exists
if not os.path.exists(likes_file):

    with open(likes_file, "w") as f:
        json.dump({"count": 0}, f)

# Load likes safely
try:

    with open(likes_file, "r") as f:

        content = f.read().strip()

        if not content:

            likes_data = {"count": 0}

        else:

            likes_data = json.loads(content)

except json.JSONDecodeError:

    likes_data = {"count": 0}

    with open(likes_file, "w") as f:

        json.dump(likes_data, f)

love_count = likes_data["count"]

# =========================================================
# HEADER LAYOUT
# =========================================================

title_col, like_col = st.columns([6, 2])

with title_col:

    st.markdown(
        "<h1 style='margin-top:15px;'>🎓 AI Career Guidance Agent</h1>",
        unsafe_allow_html=True
    )

with like_col:
    st.markdown("""
<style>

/* =====================================================
GLOBAL BUTTON STYLING
===================================================== */

.stButton > button {

    background-color: #2563eb;
    color: white;

    border: none;
    border-radius: 10px;

    padding: 0.6rem 1rem;

    font-size: 15px;
    font-weight: 600;

    transition: all 0.2s ease-in-out;

    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

/* Hover Effect */

.stButton > button:hover {

    background-color: #1d4ed8;
    color: white;

    transform: translateY(-1px);

    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

/* Click Effect */

.stButton > button:active {

    transform: scale(0.98);
}

/* Remove ugly default border */

.stButton > button:focus {

    outline: none !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)

    

    # =====================================================
    # LIKE BUTTON
    # =====================================================

    if st.button("👍 Like This App"):

        love_count += 1

        with open(likes_file, "w") as f:

            json.dump({"count": love_count}, f)

        st.rerun()

    st.caption(f"👍 {love_count} Likes")


# =========================================================
# CHECK DATA EXISTS
# =========================================================

if career_data:

    # =====================================================
    # DROPDOWNS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        qualification = st.selectbox(
            "Qualification",
            list(career_data.keys())
        )

    with col2:

        stream_options = list(
            career_data[qualification].keys()
        )

        selected_stream = st.selectbox(
            "Stream",
            stream_options
        )

    with col3:

        category_options = list(
            career_data[qualification][selected_stream].keys()
        )

        selected_category = st.selectbox(
            "Category",
            category_options
        )

    with col4:

        degree_options = list(
            career_data[qualification][selected_stream][selected_category].keys()
        )

        selected_degree = st.selectbox(
            "Degree",
            degree_options
        )

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    pg_courses = career_data[
        qualification
    ][selected_stream][selected_category][selected_degree]["Post Graduation"]

    jobs = career_data[
        qualification
    ][selected_stream][selected_category][selected_degree]["Jobs"]

    st.divider()

    result1, result2 = st.columns(2)

    with result1:

        st.subheader("🎓 Post Graduation")

        for pg in pg_courses:
            st.success(pg)

    with result2:

        st.subheader("💼 Job Opportunities")

        for job in jobs:
            st.info(job)

else:

    st.warning("No Career Data Available")

# =========================================================
# ADD NEW DATA
# =========================================================

st.divider()

st.header("➕ Add New Career Information")

with st.expander("Add Career Details"):

    new_qualification = st.text_input("Qualification")

    new_stream = st.text_input("Stream")

    new_category = st.text_input("Category")

    new_degree = st.text_input("Degree")

    new_pg = st.text_input("Post Graduation")

    new_job = st.text_input("Job Opportunity")

    if st.button("Save Career Data"):

        # =================================================
        # CREATE STRUCTURE
        # =================================================

        if new_qualification not in career_data:
            career_data[new_qualification] = {}

        if new_stream not in career_data[new_qualification]:
            career_data[new_qualification][new_stream] = {}

        if new_category not in career_data[new_qualification][new_stream]:
            career_data[new_qualification][new_stream][new_category] = {}

        if new_degree not in career_data[new_qualification][new_stream][new_category]:

            career_data[new_qualification][new_stream][new_category][new_degree] = {
                "Post Graduation": [],
                "Jobs": []
            }

        # =================================================
        # ADD DATA
        # =================================================

        if new_pg:

            career_data[new_qualification][new_stream][new_category][new_degree]["Post Graduation"].append(new_pg)

        if new_job:

            career_data[new_qualification][new_stream][new_category][new_degree]["Jobs"].append(new_job)

        # =================================================
        # SAVE TO JSON
        # =================================================

        with open(json_file, "w") as f:

            json.dump(career_data, f, indent=4)

        st.success("Career Data Saved Successfully!")
