"""Streamlit Dashboard for Smart Salary Predictor System."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json

from configs.config import (
    INCOME_MODEL_CONFIG, 
    SALARY_MODEL_CONFIG, 
    HISTORY_FILE,
    RAW_DATA_DIR,
    ARTIFACTS_DIR
)
from src.visualization.visualizer import Visualizer
from src.utils.helpers import get_prediction_history

# Page configuration
st.set_page_config(
    page_title="Smart Salary Predictor Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.875rem;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

@st.cache_data
def load_income_data():
    """Load income dataset."""
    try:
        adult_path = RAW_DATA_DIR / "adult.csv"
        if adult_path.exists():
            df = pd.read_csv(adult_path)
            if 'income' in df.columns and df['income'].dtype == 'object':
                df['income'] = df['income'].apply(lambda x: 1 if '>50K' in str(x) else 0)
            return df
    except Exception as e:
        st.error(f"Error loading income data: {e}")
    return None

@st.cache_data
def load_salary_data():
    """Load salary dataset."""
    try:
        salary_path = RAW_DATA_DIR / "salary_data.csv"
        if salary_path.exists():
            return pd.read_csv(salary_path)
    except Exception as e:
        st.error(f"Error loading salary data: {e}")
    return None

def get_model_status():
    """Get model status from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/model-status", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def main():
    """Main dashboard function."""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/money.png", width=80)
        st.title("💼 Salary Predictor")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Select Dashboard",
            ["📊 Overview", "👥 Income Analytics", "💰 Salary Analytics", "🔍 Feature Importance", 
             "📈 Model Performance", "📝 Prediction History", "⚙️ Admin"]
        )
        
        st.markdown("---")
        
        # Model Status
        model_status = get_model_status()
        if model_status:
            st.subheader("Model Status")
            col1, col2 = st.columns(2)
            with col1:
                status_color = "🟢" if model_status['income_model_loaded'] else "🔴"
                st.write(f"{status_color} Income Classifier")
            with col2:
                status_color = "🟢" if model_status['salary_model_loaded'] else "🔴"
                st.write(f"{status_color} Salary Regressor")
        
        st.markdown("---")
        st.info("Built with ❤️ using FastAPI, React & Streamlit")
    
    # Load data
    income_df = load_income_data()
    salary_df = load_salary_data()
    visualizer = Visualizer()
    
    # Page Content
    if page == "📊 Overview":
        show_overview(income_df, salary_df, model_status)
    elif page == "👥 Income Analytics":
        show_income_analytics(income_df, visualizer)
    elif page == "💰 Salary Analytics":
        show_salary_analytics(salary_df, visualizer)
    elif page == "🔍 Feature Importance":
        show_feature_importance()
    elif page == "📈 Model Performance":
        show_model_performance()
    elif page == "📝 Prediction History":
        show_prediction_history()
    elif page == "⚙️ Admin":
        show_admin_panel()

def show_overview(income_df, salary_df, model_status):
    """Show overview dashboard."""
    visualizer = Visualizer()
    st.markdown('<p class="main-header">Smart Salary Predictor Dashboard</p>', unsafe_allow_html=True)
    st.markdown("Real-time analytics and insights from ML-powered salary prediction models")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Income Dataset Size</div>
            </div>
        """.format(len(income_df) if income_df is not None else "N/A"), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-value">{}</div>
                <div class="metric-label">Salary Dataset Size</div>
            </div>
        """.format(len(salary_df) if salary_df is not None else "N/A"), unsafe_allow_html=True)
    
    with col3:
        high_income_pct = 0
        if income_df is not None:
            high_income_pct = (income_df['income'].sum() / len(income_df)) * 100
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-value">{:.1f}%</div>
                <div class="metric-label">High Income Rate</div>
            </div>
        """.format(high_income_pct), unsafe_allow_html=True)
    
    with col4:
        avg_salary = 0
        if salary_df is not None:
            avg_salary = salary_df['salary'].mean()
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-value">${:,.0f}</div>
                <div class="metric-label">Average Salary</div>
            </div>
        """.format(avg_salary), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Visualizations
    if income_df is not None and salary_df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Income Distribution")
            fig = visualizer.plot_income_distribution(income_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Salary Distribution")
            fig = visualizer.plot_salary_distribution(salary_df)
            st.plotly_chart(fig, use_container_width=True)
    
    # About Section
    st.markdown("---")
    st.subheader("About the System")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Income Classification Model
        - **Type**: Binary Classification
        - **Target**: Income >$50K or <=$50K
        - **Features**: Age, Education, Occupation, Work Class, Gender, Hours/Week
        - **Algorithms**: Logistic Regression, Decision Tree, Random Forest
        - **Best Model**: Auto-selected by F1-score
        """)
    
    with col2:
        st.markdown("""
        ### 💵 Salary Regression Model
        - **Type**: Regression
        - **Target**: Exact Salary Amount
        - **Features**: Job Title, Experience, Skills, Industry, Location
        - **Algorithms**: Linear Regression, Decision Tree, Random Forest
        - **Best Model**: Auto-selected by R² Score
        """)

def show_income_analytics(income_df, visualizer):
    """Show income analytics."""
    st.markdown('<p class="main-header">👥 Income Analytics</p>', unsafe_allow_html=True)
    
    if income_df is None:
        st.warning("Income data not available. Please train the model first.")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Education Analysis", "Occupation Analysis", "Demographics", "Correlation"])
    
    with tab1:
        st.subheader("Education vs Income")
        fig = visualizer.plot_education_vs_income(income_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Education statistics
        st.markdown("---")
        st.subheader("Education Statistics")
        edu_stats = income_df.groupby('education').agg({
            'income': ['mean', 'count']
        }).round(3)
        edu_stats.columns = ['High Income Rate', 'Count']
        edu_stats = edu_stats.sort_values('High Income Rate', ascending=False)
        st.dataframe(edu_stats, use_container_width=True)
    
    with tab2:
        st.subheader("Occupation vs Income")
        fig = visualizer.plot_occupation_vs_income(income_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Occupation statistics
        st.markdown("---")
        st.subheader("Occupation Statistics")
        occ_stats = income_df.groupby('occupation').agg({
            'income': ['mean', 'count'],
            'hours-per-week': 'mean'
        }).round(3)
        occ_stats.columns = ['High Income Rate', 'Count', 'Avg Hours/Week']
        occ_stats = occ_stats.sort_values('High Income Rate', ascending=False)
        st.dataframe(occ_stats, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Age Distribution by Income")
            fig = visualizer.plot_age_vs_income(income_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Gender Distribution")
            gender_income = pd.crosstab(income_df['gender'], income_df['income'], normalize='index') * 100
            fig = px.bar(
                gender_income,
                barmode='group',
                labels={'value': 'Percentage', 'gender': 'Gender'},
                color_discrete_map={0: '#FF6B6B', 1: '#4ECDC4'}
            )
            fig.update_layout(title="Gender vs Income Class")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Feature Correlations")
        # Select numeric columns
        numeric_cols = income_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = income_df[numeric_cols].corr()
            fig = px.imshow(
                corr_matrix,
                labels=dict(color="Correlation"),
                color_continuous_scale='RdBu',
                aspect="auto"
            )
            fig.update_layout(title="Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)

def show_salary_analytics(salary_df, visualizer):
    """Show salary analytics."""
    st.markdown('<p class="main-header">💰 Salary Analytics</p>', unsafe_allow_html=True)
    
    if salary_df is None:
        st.warning("Salary data not available. Please train the model first.")
        return
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Industry Analysis", "Experience vs Salary", "Remote Work", "Certifications"])
    
    with tab1:
        st.subheader("Industry Salary Comparison")
        fig = visualizer.plot_industry_salary_comparison(salary_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Industry statistics
        st.markdown("---")
        st.subheader("Industry Statistics")
        ind_stats = salary_df.groupby('industry').agg({
            'salary': ['mean', 'median', 'std', 'count']
        }).round(0)
        ind_stats.columns = ['Mean Salary', 'Median Salary', 'Std Dev', 'Count']
        ind_stats = ind_stats.sort_values('Mean Salary', ascending=False)
        st.dataframe(ind_stats, use_container_width=True)
    
    with tab2:
        st.subheader("Experience vs Salary")
        fig = visualizer.plot_experience_vs_salary(salary_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Experience bins analysis
        st.markdown("---")
        st.subheader("Experience Level Analysis")
        salary_df['exp_range'] = pd.cut(salary_df['experience_years'], 
                                        bins=[0, 2, 5, 10, 15, 25],
                                        labels=['0-2 years', '2-5 years', '5-10 years', '10-15 years', '15+ years'])
        exp_stats = salary_df.groupby('exp_range')['salary'].agg(['mean', 'median', 'count']).round(0)
        st.dataframe(exp_stats, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Remote Work Effect")
            fig = visualizer.plot_remote_work_effect(salary_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Remote Work Statistics")
            remote_stats = salary_df.groupby('remote_work').agg({
                'salary': ['mean', 'median', 'count']
            }).round(0)
            remote_stats.columns = ['Mean Salary', 'Median Salary', 'Count']
            st.dataframe(remote_stats, use_container_width=True)
    
    with tab4:
        st.subheader("Certification Impact on Salary")
        fig = visualizer.plot_certification_impact(salary_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Job title analysis
        st.markdown("---")
        st.subheader("Job Title Salary Analysis")
        job_fig = visualizer.plot_job_title_salary(salary_df)
        st.plotly_chart(job_fig, use_container_width=True)

def show_feature_importance():
    """Show feature importance."""
    st.markdown('<p class="main-header">🔍 Feature Importance</p>', unsafe_allow_html=True)
    
    st.info("Feature importance shows which variables have the most influence on predictions. Higher values indicate more important features.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Income Classifier - Feature Importance")
        try:
            response = requests.get(f"{API_BASE_URL}/feature-importance/income", timeout=5)
            if response.status_code == 200:
                data = response.json()
                importance = data.get('feature_importance', {})
                if importance:
                    importance_df = pd.DataFrame(
                        list(importance.items()),
                        columns=['Feature', 'Importance']
                    ).sort_values('Importance', ascending=True).tail(15)
                    
                    fig = px.bar(
                        importance_df,
                        x='Importance',
                        y='Feature',
                        orientation='h',
                        color='Importance',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Feature importance not available for this model type")
            else:
                st.error("Could not fetch income model feature importance")
        except Exception as e:
            st.error(f"Error: {e}")
    
    with col2:
        st.subheader("Salary Regressor - Feature Importance")
        try:
            response = requests.get(f"{API_BASE_URL}/feature-importance/salary", timeout=5)
            if response.status_code == 200:
                data = response.json()
                importance = data.get('feature_importance', {})
                if importance:
                    importance_df = pd.DataFrame(
                        list(importance.items()),
                        columns=['Feature', 'Importance']
                    ).sort_values('Importance', ascending=True).tail(15)
                    
                    fig = px.bar(
                        importance_df,
                        x='Importance',
                        y='Feature',
                        orientation='h',
                        color='Importance',
                        color_continuous_scale='Plasma'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Feature importance not available for this model type")
            else:
                st.error("Could not fetch salary model feature importance")
        except Exception as e:
            st.error(f"Error: {e}")

def show_model_performance():
    """Show model performance metrics."""
    st.markdown('<p class="main-header">📈 Model Performance</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Model Training & Evaluation
    
    Both models are trained using multiple algorithms and the best performing model is automatically selected.
    
    **Income Classification Models:**
    - Logistic Regression
    - Decision Tree Classifier
    - Random Forest Classifier
    
    **Salary Regression Models:**
    - Linear Regression
    - Decision Tree Regressor
    - Random Forest Regressor
    """)
    
    st.info("Retrain models from the Admin panel to see updated performance metrics.")

def show_prediction_history():
    """Show prediction history."""
    st.markdown('<p class="main-header">📝 Prediction History</p>', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE_URL}/prediction-history", timeout=5)
        if response.status_code == 200:
            data = response.json()
            history = data.get('history', [])
            
            if history:
                st.write(f"Total Predictions: {len(history)}")
                
                # Convert to DataFrame
                df = pd.json_normalize(history)
                
                # Display
                st.dataframe(df, use_container_width=True)
                
                # Download button
                if st.button("Download as CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="prediction_history.csv",
                        mime="text/csv"
                    )
            else:
                st.info("No predictions yet. Use the prediction forms to make predictions.")
        else:
            st.error("Could not fetch prediction history")
    except Exception as e:
        st.error(f"Error: {e}")

def show_admin_panel():
    """Show admin panel."""
    st.markdown('<p class="main-header">⚙️ Admin Panel</p>', unsafe_allow_html=True)
    
    st.warning("⚠️ These operations affect the production models. Use with caution.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retrain Models")
        
        if st.button("🔄 Retrain Income Model", type="primary"):
            with st.spinner("Retraining income model..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/retrain-model?model_type=income",
                        timeout=5
                    )
                    if response.status_code == 200:
                        st.success("Income model retraining started! Check backend logs for progress.")
                    else:
                        st.error("Failed to start retraining")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.button("🔄 Retrain Salary Model", type="primary"):
            with st.spinner("Retraining salary model..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/retrain-model?model_type=salary",
                        timeout=5
                    )
                    if response.status_code == 200:
                        st.success("Salary model retraining started! Check backend logs for progress.")
                    else:
                        st.error("Failed to start retraining")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.subheader("Data Management")
        
        # Clear history
        if st.button("🗑️ Clear Prediction History", type="secondary"):
            if st.checkbox("Confirm clear all history?"):
                try:
                    response = requests.delete(f"{API_BASE_URL}/prediction-history", timeout=5)
                    if response.status_code == 200:
                        st.success("Prediction history cleared!")
                    else:
                        st.error("Failed to clear history")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        # Download predictions
        if st.button("📥 Export Predictions to CSV", type="secondary"):
            try:
                response = requests.get(f"{API_BASE_URL}/download-predictions", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Predictions exported to: {data['filepath']}")
                else:
                    st.error("Failed to export predictions")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # System Info
    st.markdown("---")
    st.subheader("System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Backend**
        - FastAPI
        - Port: 8000
        - Auto-reload: Enabled
        """)
    
    with col2:
        st.markdown("""
        **Frontend**
        - React
        - Tailwind CSS
        - Port: 3000
        """)
    
    with col3:
        st.markdown("""
        **Dashboard**
        - Streamlit
        - Port: 8501
        - Plotly Charts
        """)

if __name__ == "__main__":
    main()
