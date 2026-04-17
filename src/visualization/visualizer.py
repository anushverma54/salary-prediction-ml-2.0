"""Data visualization utilities."""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
from pathlib import Path

class Visualizer:
    """Create visualizations for the ML pipeline."""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.color_scheme = px.colors.qualitative.Set2
    
    # ==================== Income Classification Visualizations ====================
    
    def plot_income_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Plot income class distribution."""
        income_counts = df['income'].value_counts()
        labels = ['<=50K', '>50K']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=[income_counts.get(0, 0), income_counts.get(1, 0)],
            hole=0.4,
            marker_colors=['#FF6B6B', '#4ECDC4']
        )])
        
        fig.update_layout(
            title="Income Distribution",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1)
        )
        return fig
    
    def plot_education_vs_income(self, df: pd.DataFrame) -> go.Figure:
        """Plot education level vs income."""
        edu_income = pd.crosstab(df['education'], df['income'], normalize='index') * 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=edu_income.index,
            y=edu_income[0],
            name='<=50K',
            marker_color='#FF6B6B'
        ))
        fig.add_trace(go.Bar(
            x=edu_income.index,
            y=edu_income[1],
            name='>50K',
            marker_color='#4ECDC4'
        ))
        
        fig.update_layout(
            title="Education vs Income (%)",
            xaxis_title="Education Level",
            yaxis_title="Percentage",
            barmode='stack',
            xaxis_tickangle=-45
        )
        return fig
    
    def plot_occupation_vs_income(self, df: pd.DataFrame) -> go.Figure:
        """Plot occupation vs income."""
        occ_income = df.groupby('occupation')['income'].agg(['mean', 'count']).reset_index()
        occ_income = occ_income.sort_values('mean', ascending=True)
        
        fig = px.bar(
            occ_income,
            x='mean',
            y='occupation',
            orientation='h',
            color='mean',
            color_continuous_scale='RdYlGn',
            labels={'mean': 'High Income Rate', 'occupation': 'Occupation'}
        )
        fig.update_layout(title="Occupation vs High Income Rate")
        return fig
    
    def plot_age_vs_income(self, df: pd.DataFrame) -> go.Figure:
        """Plot age distribution by income."""
        fig = px.box(
            df,
            x='income',
            y='age',
            color='income',
            labels={'income': 'Income Class', 'age': 'Age'},
            color_discrete_map={0: '#FF6B6B', 1: '#4ECDC4'}
        )
        fig.update_layout(title="Age Distribution by Income Class")
        return fig
    
    # ==================== Salary Regression Visualizations ====================
    
    def plot_salary_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Plot salary distribution."""
        fig = px.histogram(
            df,
            x='salary',
            nbins=50,
            color_discrete_sequence=['#4ECDC4']
        )
        fig.update_layout(
            title="Salary Distribution",
            xaxis_title="Salary ($)",
            yaxis_title="Count"
        )
        return fig
    
    def plot_experience_vs_salary(self, df: pd.DataFrame) -> go.Figure:
        """Plot experience years vs salary."""
        fig = px.scatter(
            df,
            x='experience_years',
            y='salary',
            color='job_title',
            opacity=0.6,
            trendline='ols'
        )
        fig.update_layout(
            title="Experience vs Salary",
            xaxis_title="Years of Experience",
            yaxis_title="Salary ($)"
        )
        return fig
    
    def plot_industry_salary_comparison(self, df: pd.DataFrame) -> go.Figure:
        """Plot industry vs average salary."""
        industry_salary = df.groupby('industry').agg({
            'salary': ['mean', 'median', 'count']
        }).reset_index()
        industry_salary.columns = ['industry', 'mean_salary', 'median_salary', 'count']
        industry_salary = industry_salary.sort_values('mean_salary', ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=industry_salary['industry'],
            x=industry_salary['mean_salary'],
            orientation='h',
            name='Mean Salary',
            marker_color='#4ECDC4'
        ))
        fig.add_trace(go.Bar(
            y=industry_salary['industry'],
            x=industry_salary['median_salary'],
            orientation='h',
            name='Median Salary',
            marker_color='#45B7D1'
        ))
        
        fig.update_layout(
            title="Industry Salary Comparison",
            xaxis_title="Salary ($)",
            yaxis_title="Industry",
            barmode='group'
        )
        return fig
    
    def plot_remote_work_effect(self, df: pd.DataFrame) -> go.Figure:
        """Plot remote work effect on salary."""
        remote_salary = df.groupby('remote_work')['salary'].agg(['mean', 'median', 'std']).reset_index()
        
        fig = px.bar(
            remote_salary,
            x='remote_work',
            y='mean',
            error_y='std',
            color='remote_work',
            labels={'mean': 'Average Salary', 'remote_work': 'Work Type'}
        )
        fig.update_layout(title="Remote Work vs Average Salary")
        return fig
    
    def plot_certification_impact(self, df: pd.DataFrame) -> go.Figure:
        """Plot certification impact on salary."""
        cert_salary = df.groupby('certifications')['salary'].agg(['mean', 'count']).reset_index()
        cert_salary = cert_salary.sort_values('mean', ascending=False)
        
        fig = px.bar(
            cert_salary,
            x='certifications',
            y='mean',
            color='mean',
            color_continuous_scale='Viridis',
            labels={'mean': 'Average Salary', 'certifications': 'Certifications'}
        )
        fig.update_layout(
            title="Certification Impact on Salary",
            xaxis_tickangle=-45
        )
        return fig
    
    def plot_job_title_salary(self, df: pd.DataFrame) -> go.Figure:
        """Plot job title vs salary."""
        job_salary = df.groupby('job_title').agg({
            'salary': ['mean', 'median']
        }).reset_index()
        job_salary.columns = ['job_title', 'mean_salary', 'median_salary']
        job_salary = job_salary.sort_values('mean_salary', ascending=True).tail(15)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=job_salary['mean_salary'],
            y=job_salary['job_title'],
            mode='markers',
            marker=dict(size=12, color='#4ECDC4'),
            name='Mean Salary'
        ))
        
        fig.update_layout(
            title="Top 15 Job Titles by Salary",
            xaxis_title="Salary ($)",
            yaxis_title="Job Title"
        )
        return fig
    
    # ==================== Feature Importance Visualizations ====================
    
    def plot_feature_importance(self, importance_dict: Dict[str, float], title: str = "Feature Importance") -> go.Figure:
        """Plot feature importance."""
        importance_df = pd.DataFrame(
            list(importance_dict.items()),
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
        fig.update_layout(title=title)
        return fig
    
    def plot_confusion_matrix(self, cm: np.ndarray, labels: List[str] = None) -> go.Figure:
        """Plot confusion matrix."""
        if labels is None:
            labels = ['<=50K', '>50K']
        
        fig = px.imshow(
            cm,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=labels,
            y=labels,
            color_continuous_scale='Blues',
            text_auto=True
        )
        fig.update_layout(title="Confusion Matrix")
        return fig
    
    # ==================== Model Performance Visualizations ====================
    
    def plot_model_comparison(self, comparison_df: pd.DataFrame, model_type: str = "classification") -> go.Figure:
        """Plot model comparison metrics."""
        if model_type == "classification":
            metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        else:
            metrics = ['mae', 'rmse', 'r2_score']
        
        fig = make_subplots(
            rows=1,
            cols=len(metrics),
            subplot_titles=metrics
        )
        
        for i, metric in enumerate(metrics, 1):
            fig.add_trace(
                go.Bar(
                    x=comparison_df['Model'],
                    y=comparison_df[metric],
                    name=metric
                ),
                row=1, col=i
            )
        
        fig.update_layout(
            title="Model Comparison",
            showlegend=False,
            height=400
        )
        return fig
    
    # ==================== Static Plots (for reports) ====================
    
    def save_plot(self, fig: go.Figure, filepath: Path) -> None:
        """Save plotly figure to HTML."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(filepath)
        if self.logger:
            self.logger.info(f"Plot saved to {filepath}")
    
    def create_correlation_heatmap(self, df: pd.DataFrame, filepath: Path = None) -> plt.Figure:
        """Create correlation heatmap using seaborn."""
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap='coolwarm',
            center=0,
            fmt='.2f'
        )
        plt.title("Feature Correlation Heatmap")
        plt.tight_layout()
        
        if filepath:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
        
        return plt.gcf()
