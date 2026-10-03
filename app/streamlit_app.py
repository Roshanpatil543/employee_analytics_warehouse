from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app.db_manager import DatabaseConnection
from app.managers import AnalyticsManager, EmployeeManager, ProjectManager
from app.models import Employee, Project

st.set_page_config(page_title="Employee Analytics", page_icon="📊", layout="wide")


@st.cache_data
def load_sample_metrics():
    return pd.DataFrame(
        {
            "review_year": [2022, 2023, 2024, 2025],
            "avg_score": [81.2, 84.4, 86.7, 89.5],
        }
    )


@st.cache_data
def load_sample_top_performers():
    return pd.DataFrame(
        {
            "employee_id": [101, 203, 156, 287],
            "first_name": ["Alicia", "Daniel", "Priya", "Morgan"],
            "last_name": ["Stone", "Nguyen", "Rao", "West"],
            "department_name": ["Engineering", "Sales", "Finance", "Operations"],
            "overall_score": [96, 94, 92, 91],
            "dept_rank": [1, 1, 1, 1],
        }
    )


def safe_fetch(manager, method_name, fallback):
    try:
        result = getattr(manager, method_name)()
        return result if result else fallback
    except Exception:
        return fallback


st.title("Enterprise Employee Analytics & Data Warehouse")

sidebar = st.sidebar
sidebar.header("Navigation")
page = sidebar.radio("Choose a module", ["Overview", "Employee Onboarding", "Project Management", "Analytics Dashboard"])

if page == "Overview":
    st.subheader("Platform Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Employees", "100,000+")
    col2.metric("Departments", "8")
    col3.metric("Performance Score", "89.5")

    metrics = load_sample_metrics()
    fig = px.line(metrics, x="review_year", y="avg_score", markers=True, title="Year-over-Year Performance")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Employee Onboarding":
    st.subheader("Onboard Employee")
    with st.form("employee_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        department_id = st.number_input("Department ID", min_value=1, step=1)
        job_title = st.text_input("Job Title")
        salary = st.number_input("Salary", min_value=30000.0, step=500.0)
        submitted = st.form_submit_button("Add Employee")

    if submitted:
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=int(department_id),
            job_title=job_title,
            salary=float(salary),
        )
        try:
            manager = EmployeeManager()
            employee_id = manager.create_employee(employee)
            st.success(f"Employee added successfully with ID {employee_id}.")
        except Exception as exc:
            st.error(f"Unable to add employee: {exc}")

elif page == "Project Management":
    st.subheader("Create Project")
    with st.form("project_form"):
        project_name = st.text_input("Project Name")
        department_id = st.number_input("Department ID", min_value=1, step=1)
        budget = st.number_input("Budget", min_value=0.0, step=1000.0)
        submitted = st.form_submit_button("Create Project")

    if submitted:
        project = Project(project_name=project_name, department_id=int(department_id), budget=float(budget))
        try:
            manager = ProjectManager()
            project_id = manager.create_project(project)
            st.success(f"Project created successfully with ID {project_id}.")
        except Exception as exc:
            st.error(f"Unable to create project: {exc}")

else:
    st.subheader("Analytics Dashboard")
    try:
        analytics = AnalyticsManager()
        series = safe_fetch(analytics, "get_performance_trends", load_sample_metrics().to_dict("records"))
        top = safe_fetch(analytics, "get_top_performers", load_sample_top_performers().to_dict("records"))
        risk = safe_fetch(analytics, "get_attrition_risk", [
            {"department_name": "Engineering", "employees": 1200, "avg_performance": 88},
            {"department_name": "Sales", "employees": 980, "avg_performance": 80},
        ])

        trend_df = pd.DataFrame(series)
        top_df = pd.DataFrame(top)
        risk_df = pd.DataFrame(risk)

        if not trend_df.empty:
            trend_fig = px.line(trend_df, x="review_year", y="avg_score", markers=True, title="Performance Trend")
            st.plotly_chart(trend_fig, use_container_width=True)

        if not top_df.empty:
            top_fig = px.bar(top_df, x="first_name", y="overall_score", color="department_name", title="Top Performers by Department")
            st.plotly_chart(top_fig, use_container_width=True)

        if not risk_df.empty:
            risk_fig = px.bar(risk_df, x="department_name", y="employees", color="avg_performance", title="Attrition Risk View")
            st.plotly_chart(risk_fig, use_container_width=True)

    except Exception as exc:
        st.warning(f"Database not reachable; showing sample analytics. Details: {exc}")
        trend_df = load_sample_metrics()
        top_df = load_sample_top_performers()
        st.plotly_chart(px.line(trend_df, x="review_year", y="avg_score", markers=True), use_container_width=True)
        st.plotly_chart(px.bar(top_df, x="first_name", y="overall_score", color="department_name"), use_container_width=True)
