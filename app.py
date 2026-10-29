import streamlit as st
import pandas as pd
import os
from google import genai
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)
st.set_page_config(
    page_title="Student Performance Analysis System",
    page_icon="🎓",
    layout="wide"
)
FILE_NAME = "student_data.csv"
st.title("🎓 AI-Powered Student Performance Analysis System")
st.write("Enter student details to analyze academic performance.")
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=[
        "Name",
        "Maths",
        "Science",
        "English",
        "Attendance",
        "Study Hours",
        "Average Marks"
    ])
def get_performance_category(marks):
    if marks >= 80:
        return "Excellent"
    elif marks >= 60:
        return "Good"
    elif marks >= 40:
        return "Average"
    else:
        return "Needs Improvement"


if not df.empty:
    df["Performance Category"] = df["Average Marks"].apply(
        get_performance_category
    )
    df.to_csv(FILE_NAME, index=False)
st.subheader("Add Student Details")
with st.form("student_form"):
    name = st.text_input("Student Name")
    col1, col2, col3 = st.columns(3)
    with col1:
        maths = st.number_input("Maths Marks", min_value=0, max_value=100, value=0)
    with col2:
        science = st.number_input("Science Marks", min_value=0, max_value=100, value=0)
    with col3:
        english = st.number_input("English Marks", min_value=0, max_value=100, value=0)
    attendance = st.number_input(
        "Attendance (%)",
        min_value=0,
        max_value=100,
        value=0
    )
    study_hours = st.number_input(
        "Daily Study Hours",
        min_value=0.0,
        max_value=24.0,
        value=1.0,
        step=0.5
    )
    submitted = st.form_submit_button("Add Student")
    if submitted:
        if name.strip() == "":
            st.error("Please enter the student name.")
        else:
            average = (maths + science + english) / 3
            average = round(average, 2)
            new_student = pd.DataFrame([{
                "Name": name.strip(),
                "Maths": maths,
                "Science": science,
                "English": english,
                "Attendance": attendance,
                "Study Hours": study_hours,
                "Average Marks": average,
                "Performance Category": get_performance_category(average)
                }])
            df = pd.concat([df, new_student], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success(f"Student {name.strip()} added successfully!")
            st.rerun()
st.divider()
st.subheader("Student Records")

if not df.empty:

    search_name = st.text_input("🔍 Search Student by Name")

    col1, col2 = st.columns(2)

    with col1:
        min_marks = st.slider(
            "Minimum Average Marks",
            min_value=0,
            max_value=100,
            value=0
        )

    with col2:
        min_attendance = st.slider(
            "Minimum Attendance (%)",
            min_value=0,
            max_value=100,
            value=0
        )

    filtered_df = df.copy()

    if search_name:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(
                search_name,
                case=False,
                na=False
            )
        ]

    filtered_df = filtered_df[
        (filtered_df["Average Marks"] >= min_marks) &
        (filtered_df["Attendance"] >= min_attendance)
    ]

    st.dataframe(filtered_df, use_container_width=True)

    st.write("Students Found:", len(filtered_df))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", len(df))

    with col2:
        if not filtered_df.empty:
            st.metric(
                "Filtered Average Marks",
                f"{filtered_df['Average Marks'].mean():.2f}"
            )
        else:
            st.metric("Filtered Average Marks", "N/A")

    with col3:
        if not filtered_df.empty:
            st.metric(
                "Filtered Average Attendance",
                f"{filtered_df['Attendance'].mean():.2f}%"
            )
        else:
            st.metric("Filtered Average Attendance", "N/A")

else:
    st.info("No student records available. Please add a student first.")
st.subheader("Subject-Wise Performance")

if not df.empty:
    import matplotlib.pyplot as plt

    selected_student = st.selectbox(
        "Select Student",
        df["Name"].unique()
    )

    student = df[df["Name"] == selected_student].iloc[0]

    subjects = ["Maths", "Science", "English"]
    marks = [
        student["Maths"],
        student["Science"],
        student["English"]
    ]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(subjects, marks)

    ax.set_title(f"Subject-Wise Marks: {selected_student}")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_ylim(0, 100)
    ax.bar_label(bars)

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Student Average Marks")

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.bar(df["Name"], df["Average Marks"])

    ax.set_title("Average Marks of Students")
    ax.set_xlabel("Students")
    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)
    ax.bar_label(bars, fmt="%.2f")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
st.divider()
st.header("📊 Data Science Analysis")

if not df.empty:
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    st.subheader("1. Statistical Summary")

    numeric_columns = [
        "Maths",
        "Science",
        "English",
        "Attendance",
        "Study Hours",
        "Average Marks"
    ]

    summary = df[numeric_columns].describe().round(2)
    st.dataframe(summary, use_container_width=True)

    st.subheader("2. Subject-Wise Average Marks")

    subject_averages = df[["Maths", "Science", "English"]].mean().round(2)

    st.bar_chart(subject_averages)

    st.subheader("3. Study Hours vs Average Marks")

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.scatterplot(
        data=df,
        x="Study Hours",
        y="Average Marks",
        hue="Performance Category",
        ax=ax
    )

    ax.set_title("Relationship Between Study Hours and Marks")
    ax.set_xlabel("Daily Study Hours")
    ax.set_ylabel("Average Marks")

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("4. Attendance vs Average Marks")

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.scatterplot(
        data=df,
        x="Attendance",
        y="Average Marks",
        hue="Performance Category",
        ax=ax
    )

    ax.set_title("Relationship Between Attendance and Marks")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Average Marks")

    st.pyplot(fig)
    plt.close(fig)

else:
    st.info("Add student records to view Data Science Analysis.")
st.divider()
st.header("🤖 Machine Learning Performance Prediction")

if len(df) < 5:
    st.warning(
        "Please add at least 5 student records before using this feature."
    )
else:
    from sklearn.ensemble import RandomForestRegressor

    st.write(
        "Enter student details to estimate their average marks "
        "using a machine learning model."
    )

    features = [
        "Maths",
        "Science",
        "English",
        "Attendance",
        "Study Hours"
    ]

    X = df[features]
    y = df["Average Marks"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    st.subheader("Enter Student Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        pred_maths = st.number_input(
            "Prediction: Maths Marks",
            min_value=0,
            max_value=100,
            value=70,
            key="pred_maths"
        )

    with col2:
        pred_science = st.number_input(
            "Prediction: Science Marks",
            min_value=0,
            max_value=100,
            value=70,
            key="pred_science"
        )

    with col3:
        pred_english = st.number_input(
            "Prediction: English Marks",
            min_value=0,
            max_value=100,
            value=70,
            key="pred_english"
        )

    pred_attendance = st.number_input(
        "Prediction: Attendance (%)",
        min_value=0,
        max_value=100,
        value=80,
        key="pred_attendance"
    )

    pred_study_hours = st.number_input(
        "Prediction: Daily Study Hours",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.5,
        key="pred_study_hours"
    )

    if st.button("Predict Student Performance"):

        input_data = pd.DataFrame([{
            "Maths": pred_maths,
            "Science": pred_science,
            "English": pred_english,
            "Attendance": pred_attendance,
            "Study Hours": pred_study_hours
        }])

        prediction = model.predict(input_data)[0]
        prediction = max(0, min(100, prediction))

        category = get_performance_category(prediction)

        st.success("Prediction completed!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Predicted Average Marks",
                f"{prediction:.2f}/100"
            )

        with col2:
            st.metric(
                "Predicted Performance Category",
                category
            )

        st.info(
            "This is an estimate from a model trained on your current "
            "dataset. Its reliability depends on the amount and quality "
            "of the available data."
        )

st.divider()
st.header("📚 Smart Study Assistant")
if not df.empty:
    student_names = df["Name"].dropna().unique().tolist()

    selected_ai_student = st.selectbox(
        "Select Student for AI Analysis",
        student_names,
        key="ai_student_select"
    )

    selected_student_data = df[
        df["Name"] == selected_ai_student
    ].iloc[0]
else:
    selected_ai_student = None
    selected_student_data = None
    st.info("Add a student record to use personalized AI analysis.")
st.write(
    "Get personalized study guidance using Gemini AI. "
    "Ask questions about subjects, concepts, or study planning."
)

subject = st.selectbox(
    "Select Subject",
    [
        "Maths",
        "Science",
        "English",
        "Computer Science",
        "Data Science",
        "Artificial Intelligence",
        "Other"
    ]
)

study_question = st.text_area(
    "What would you like help with?",
    placeholder="Example: Explain Python lists with an example."
)

available_hours = st.number_input(
    "Available study hours per day",
    min_value=1,
    max_value=12,
    value=3
)

if st.button("Generate Study Guidance"):

    if not study_question.strip():
        st.warning("Please enter your study question.")

    else:
        try:
            with st.spinner("Gemini AI is preparing your guidance..."):

                if selected_student_data is not None:
                    student_context = f"""
                    Student Name: {selected_student_data['Name']}
                    Maths Marks: {selected_student_data['Maths']}
                    Science Marks: {selected_student_data['Science']}
                    English Marks: {selected_student_data['English']}
                    Average Marks: {selected_student_data['Average Marks']}
                    Attendance: {selected_student_data['Attendance']}%
                    Daily Study Hours: {selected_student_data['Study Hours']}
                    Performance Category: {selected_student_data['Performance Category']}
                    """
                else:
                    student_context = "No student record is available."

                prompt = f"""
                You are a helpful educational study assistant.

                Student Academic Record:
                {student_context}

                Selected Subject: {subject}
                Student's Question: {study_question}
                Available Study Hours Per Day: {available_hours}

                If the student asks for performance analysis,
                use the academic record provided above.

                Identify areas for improvement and suggest practical,
                personalized study strategies.

                Do not invent marks or student information.
                If no student record is available, explain that
                actual academic data is needed for personalized analysis.

                Use simple English, headings, and examples where useful.
                Make study plans that fit the available study hours.
                """

                response = client.interactions.create(
                    model="gemini-3.5-flash-lite",
                    input=prompt
                )

            st.subheader("Your AI Study Guidance")
            if hasattr(response, "output_text") and response.output_text:
                st.markdown(response.output_text)
                st.success("Study guidance generated successfully!")
            elif hasattr(response, "text") and response.text:
                st.markdown(response.text)
                st.success("Study guidance generated successfully!")
            else:
                st.warning(
                    "Gemini returned a response, but no text was found. "
                    "Please try again."
                )
        except Exception as e:
            st.error(
                "Unable to generate study guidance. "
                "Please try again or check your Gemini API settings."
            )
            st.caption(f"Error details: {e}")