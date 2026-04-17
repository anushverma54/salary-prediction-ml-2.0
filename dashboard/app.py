"""Streamlit Salary Predictor - All-in-One Dashboard with Predictions."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime

from configs.config import (
    SALARY_MODEL_CONFIG,
    HISTORY_FILE,
    RAW_DATA_DIR,
    ARTIFACTS_DIR
)
from src.visualization.visualizer import Visualizer
from src.utils.helpers import get_prediction_history, setup_logging

# Page configuration
st.set_page_config(
    page_title="Smart Salary Predictor",
    page_icon="💰",
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
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .salary-amount {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

API_BASE_URL = "http://localhost:8000"

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

def predict_salary(data):
    """Make salary prediction via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/predict-salary", json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Prediction error: {e}")
    return None

def get_feature_importance():
    """Get feature importance from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/feature-importance", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def main():
    """Main application."""
    
    # Sidebar Navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/money.png", width=80)
        st.title("💰 Salary Predictor")
        st.markdown("---")
        
        page = st.radio(
            "Navigate",
            ["🔮 Predict Salary", "📊 Analytics", "🔍 Feature Importance", "📈 Model Performance", "⚙️ Admin"]
        )
        
        st.markdown("---")
        
        # Model Status
        model_status = get_model_status()
        if model_status:
            st.subheader("Model Status")
            if model_status.get('salary_model_loaded'):
                st.success("✅ Salary Model Ready")
            else:
                st.error("❌ Model Not Loaded")
        
        st.markdown("---")
        st.info("ML-Powered Salary Prediction")
    
    # Load data
    salary_df = load_salary_data()
    
    # Page Routing
    if page == "🔮 Predict Salary":
        show_prediction_page()
    elif page == "📊 Analytics":
        show_analytics(salary_df)
    elif page == "🔍 Feature Importance":
        show_feature_importance_page()
    elif page == "📈 Model Performance":
        show_model_performance()
    elif page == "⚙️ Admin":
        show_admin_panel()

def show_prediction_page():
    """Show salary prediction page with popup-style results."""
    st.markdown('<p class="main-header">🔮 Salary Prediction</p>', unsafe_allow_html=True)
    
    # Initialize session state for result
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
        st.session_state.prediction_result = None
    
    # ==================== POPUP RESULT SECTION (Shown at top when available) ====================
    if st.session_state.show_result and st.session_state.prediction_result:
        result = st.session_state.prediction_result
        
        # Create a prominent "popup" container at the top
        popup_col1, popup_col2, popup_col3 = st.columns([1, 3, 1])
        
        with popup_col2:
            # Large salary card - like a popup/modal
            st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 40px; border-radius: 25px; text-align: center; 
                            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);
                            border: 4px solid rgba(255,255,255,0.2);
                            margin: 20px 0;">
                    <div style="color: rgba(255,255,255,0.9); font-size: 16px; 
                                text-transform: uppercase; letter-spacing: 3px; margin-bottom: 15px;">
                        🎉 Your Predicted Annual Salary
                    </div>
                    <div style="color: white; font-size: 56px; font-weight: bold; 
                                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                        ${:,.0f}
                    </div>
                </div>
            """.format(result["prediction"]), unsafe_allow_html=True)
            
            # Close button (X style)
            if st.button("❌ Close & Make New Prediction", use_container_width=True, type="secondary"):
                st.session_state.show_result = False
                st.session_state.prediction_result = None
                st.rerun()
        
        # Divider
        st.markdown("---")
        
        # Details in expanders (user can choose to see more)
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            with st.expander("💰 Salary Breakdown", expanded=True):
                monthly = result["prediction"] / 12
                biweekly = result["prediction"] / 26
                weekly = result["prediction"] / 52
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Monthly", f"${monthly:,.0f}")
                m2.metric("Bi-weekly", f"${biweekly:,.0f}")
                m3.metric("Weekly", f"${weekly:,.0f}")
                
                if result.get('confidence'):
                    st.progress(result['confidence'])
                    st.caption(f"🎯 Model Confidence: {result['confidence']*100:.1f}%")
        
        with col_exp2:
            with st.expander("🔍 Top Influencing Factors", expanded=True):
                if result.get('top_features'):
                    for feature in result['top_features'][:5]:
                        st.progress(feature['importance'])
                        st.caption(f"{feature['feature']}")
        
        # Comparison Chart
        with st.expander("📊 How You Compare to Market", expanded=False):
            salary_df = load_salary_data()
            if salary_df is not None:
                job_title = st.session_state.get('job_title', 'Software Engineer')
                job_avg = salary_df[salary_df['job_title'] == job_title]['salary'].mean()
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Your Prediction',
                    x=['Your Salary'],
                    y=[result['prediction']],
                    marker_color='#667eea',
                    text=[f"${result['prediction']:,.0f}"],
                    textposition='outside'
                ))
                
                fig.add_trace(go.Bar(
                    name=f'Avg {job_title}',
                    x=[f'Avg {job_title}'],
                    y=[job_avg if not pd.isna(job_avg) else result['prediction']],
                    marker_color='#94a3b8',
                    text=[f"${job_avg:,.0f}" if not pd.isna(job_avg) else "N/A"],
                    textposition='outside'
                ))
                
                fig.add_trace(go.Bar(
                    name='Market Average',
                    x=['Market Avg'],
                    y=[salary_df['salary'].mean()],
                    marker_color='#cbd5e1',
                    text=[f"${salary_df['salary'].mean():,.0f}"],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=20, r=20, t=30, b=20),
                    yaxis_title=None,
                    xaxis_title=None,
                    title="Your Salary vs Market Comparisons"
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
    
    # ==================== INPUT FORM SECTION ====================
    if not st.session_state.show_result:
        st.markdown("Enter your job details to get an AI-powered salary estimate.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("� Job Details")
            
            job_titles = ['Software Engineer', 'Data Scientist', 'Product Manager', 'DevOps Engineer',
                          'UI/UX Designer', 'Marketing Manager', 'Sales Representative', 'HR Manager',
                          'Business Analyst', 'System Administrator', 'QA Engineer', 'Data Analyst',
                          'Full Stack Developer', 'Frontend Developer', 'Backend Developer', 'ML Engineer']
            
            education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD', 'MBA']
            
            industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing', 'Education',
                          'Consulting', 'Media', 'Government', 'Energy']
            
            company_sizes = ['Startup (1-50)', 'Small (51-200)', 'Medium (201-1000)', 'Large (1000+)']
            
            locations = ['San Francisco', 'New York', 'Seattle', 'Austin', 'Boston', 'Chicago', 'Denver',
                         'Remote', 'Los Angeles', 'Washington DC', 'Atlanta', 'Dallas']
            
            remote_options = ['Fully Remote', 'Hybrid', 'On-site']
            
            certifications = ['None', 'AWS Certified', 'Google Cloud', 'Azure Certified', 'PMP',
                             'Scrum Master', 'Data Science Cert', 'Cybersecurity Cert', 'Multiple']
            
            job_title = st.selectbox("Job Title *", job_titles, key="job_title")
            industry = st.selectbox("Industry *", industries, key="industry")
            education_level = st.selectbox("Education Level *", education_levels, key="education")
            company_size = st.selectbox("Company Size *", company_sizes, key="company_size")
            location = st.selectbox("Location *", locations, key="location")
            
        with col2:
            st.subheader("� Experience & Skills")
            
            experience_years = st.slider("Years of Experience", 0, 30, 5, key="exp_years")
            skills_count = st.slider("Number of Skills", 1, 25, 8, key="skills")
            remote_work = st.selectbox("Remote Work", remote_options, key="remote")
            certifications_selected = st.selectbox("Certifications", certifications, key="certs")
            
            st.markdown("---")
            
            if st.button("🚀 Predict My Salary", use_container_width=True, type="primary"):
                data = {
                    "job_title": job_title,
                    "experience_years": experience_years,
                    "education_level": education_level,
                    "skills_count": skills_count,
                    "industry": industry,
                    "company_size": company_size,
                    "location": location,
                    "remote_work": remote_work,
                    "certifications": certifications_selected
                }
                
                with st.spinner("🧠 AI analyzing your profile..."):
                    result = predict_salary(data)
                
                if result:
                    st.session_state.prediction_result = result
                    st.session_state.show_result = True
                    st.rerun()
        
        # Market insights preview when no prediction yet
        st.markdown("---")
        with st.expander("📊 Preview Market Data"):
            salary_df = load_salary_data()
            if salary_df is not None:
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                col_m1.metric("Dataset Size", f"{len(salary_df):,}")
                col_m2.metric("Market Avg", f"${salary_df['salary'].mean():,.0f}")
                col_m3.metric("Market Median", f"${salary_df['salary'].median():,.0f}")
                col_m4.metric("Max Salary", f"${salary_df['salary'].max():,.0f}")
            else:
                st.info("Train the model to see market data")

def show_analytics(salary_df):
    """Show analytics dashboard."""
    st.markdown('<p class="main-header">📊 Salary Analytics</p>', unsafe_allow_html=True)
    
    if salary_df is None:
        st.warning("Salary data not available. Please train the model first.")
        return
    
    visualizer = Visualizer()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dataset Size", f"{len(salary_df):,}")
    col2.metric("Average Salary", f"${salary_df['salary'].mean():,.0f}")
    col3.metric("Median Salary", f"${salary_df['salary'].median():,.0f}")
    col4.metric("Max Salary", f"${salary_df['salary'].max():,.0f}")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Industry Analysis", "Experience vs Salary", "Job Titles", "Remote Work"])
    
    with tab1:
        st.subheader("Industry Salary Comparison")
        fig = visualizer.plot_industry_salary_comparison(salary_df)
        st.plotly_chart(fig, use_container_width=True)
        
        ind_stats = salary_df.groupby('industry').agg({
            'salary': ['mean', 'median', 'count']
        }).round(0)
        ind_stats.columns = ['Mean Salary', 'Median Salary', 'Count']
        ind_stats = ind_stats.sort_values('Mean Salary', ascending=False)
        st.dataframe(ind_stats, use_container_width=True)
    
    with tab2:
        st.subheader("Experience vs Salary")
        fig = visualizer.plot_experience_vs_salary(salary_df)
        st.plotly_chart(fig, use_container_width=True)
        
        salary_df['exp_range'] = pd.cut(salary_df['experience_years'], 
                                        bins=[0, 2, 5, 10, 15, 30],
                                        labels=['0-2 years', '2-5 years', '5-10 years', '10-15 years', '15+ years'])
        exp_stats = salary_df.groupby('exp_range')['salary'].agg(['mean', 'median', 'count']).round(0)
        st.dataframe(exp_stats, use_container_width=True)
    
    with tab3:
        st.subheader("Job Title Salary Analysis")
        job_salary = salary_df.groupby('job_title')['salary'].mean().sort_values(ascending=False).head(15)
        fig = px.bar(x=job_salary.values, y=job_salary.index, orientation='h',
                     color=job_salary.values, color_continuous_scale='Viridis')
        fig.update_layout(xaxis_title="Average Salary", yaxis_title="Job Title")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Remote Work Effect")
            fig = visualizer.plot_remote_work_effect(salary_df)
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            st.subheader("Certification Impact")
            fig = visualizer.plot_certification_impact(salary_df)
            st.plotly_chart(fig, use_container_width=True)

def show_feature_importance_page():
    """Show feature importance."""
    st.markdown('<p class="main-header">🔍 Feature Importance</p>', unsafe_allow_html=True)
    
    st.info("Understanding which factors most influence salary predictions.")
    
    result = get_feature_importance()
    
    if result and result.get('feature_importance'):
        importance = result['feature_importance']
        
        # Create DataFrame for visualization
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
        
        # Show as table
        st.dataframe(importance_df.sort_values('Importance', ascending=False), use_container_width=True)
    else:
        st.warning("Feature importance not available. Model may not support it.")

def show_model_performance():
    """Show model performance."""
    st.markdown('<p class="main-header">📈 Model Performance</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Salary Regression Model
    
    **Algorithms Tested:**
    - Linear Regression
    - Decision Tree Regressor  
    - Random Forest Regressor
    
    **Best Model Selected By:**
    - R² Score (higher is better)
    - Lowest RMSE (Root Mean Squared Error)
    
    **Evaluation Metrics:**
    - MAE (Mean Absolute Error)
    - RMSE (Root Mean Squared Error)
    - R² Score
    """)
    
    st.info("Retrain the model from the Admin panel to see updated performance metrics.")

def show_admin_panel():
    """Show admin panel."""
    st.markdown('<p class="main-header">⚙️ Admin Panel</p>', unsafe_allow_html=True)
    
    st.warning("⚠️ These operations affect the production model. Use with caution.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Management")
        
        if st.button("🔄 Retrain Salary Model", use_container_width=True):
            with st.spinner("Retraining model..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/retrain-model", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Model retraining started!")
                    else:
                        st.error("Failed to start retraining")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        st.markdown("---")
        
        # Upload dataset
        st.subheader("Upload New Dataset")
        uploaded_file = st.file_uploader("Upload salary_data.csv", type="csv")
        if uploaded_file:
            if st.button("Upload Dataset"):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(f"{API_BASE_URL}/upload-dataset", files=files, timeout=10)
                    if response.status_code == 200:
                        st.success("✅ Dataset uploaded successfully!")
                    else:
                        st.error("Failed to upload dataset")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.subheader("Prediction History")
        
        if st.button("📥 Export Predictions"):
            try:
                response = requests.get(f"{API_BASE_URL}/download-predictions", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Exported to: {data['filepath']}")
                else:
                    st.error("Failed to export predictions")
            except Exception as e:
                st.error(f"Error: {e}")
        
        if st.button("🗑️ Clear History"):
            if st.checkbox("Confirm deletion"):
                try:
                    response = requests.delete(f"{API_BASE_URL}/prediction-history", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ History cleared!")
                    else:
                        st.error("Failed to clear history")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # System Info
    st.markdown("---")
    st.subheader("System Information")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        **Backend**
        - FastAPI
        - Port: 8000
        - Auto-reload: Enabled
        """)
    
    with col_b:
        st.markdown("""
        **ML Pipeline**
        - scikit-learn
        - pandas
        - Regression Models
        """)
    
    with col_c:
        st.markdown("""
        **Dashboard**
        - Streamlit
        - Plotly Charts
        - Real-time API
        """)

if __name__ == "__main__":
    main()
