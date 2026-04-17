import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Users, DollarSign, AlertCircle, Loader2, Target } from 'lucide-react';
import { getModelStatus, getFeatureImportance } from '../services/api';

const Insights = () => {
  const [modelStatus, setModelStatus] = useState(null);
  const [incomeFeatures, setIncomeFeatures] = useState(null);
  const [salaryFeatures, setSalaryFeatures] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const status = await getModelStatus();
      setModelStatus(status);

      if (status.income_model_loaded) {
        try {
          const incomeImp = await getFeatureImportance('income');
          setIncomeFeatures(incomeImp.feature_importance);
        } catch (e) {
          console.log('Income feature importance not available');
        }
      }

      if (status.salary_model_loaded) {
        try {
          const salaryImp = await getFeatureImportance('salary');
          setSalaryFeatures(salaryImp.feature_importance);
        } catch (e) {
          console.log('Salary feature importance not available');
        }
      }
    } catch (err) {
      setError('Failed to load model insights. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderFeatureBars = (features) => {
    if (!features) return null;
    
    const sortedFeatures = Object.entries(features)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10);
    
    const maxValue = sortedFeatures[0]?.[1] || 1;

    return (
      <div className="space-y-3">
        {sortedFeatures.map(([feature, importance]) => (
          <div key={feature}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-700 truncate pr-4">{feature}</span>
              <span className="text-gray-500">{(importance * 100).toFixed(1)}%</span>
            </div>
            <div className="feature-bar">
              <div 
                className="feature-bar-fill"
                style={{ width: `${(importance / maxValue) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
        <span className="ml-3 text-gray-600">Loading insights...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center py-20 text-red-600">
        <AlertCircle className="w-8 h-8 mr-3" />
        <span>{error}</span>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">ML Model Insights</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Explore how our machine learning models work and what factors most influence predictions.
        </p>
      </div>

      {/* Model Status Cards */}
      <div className="grid md:grid-cols-2 gap-6 mb-10">
        <div className="card">
          <div className="flex items-center space-x-4 mb-4">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
              modelStatus?.income_model_loaded ? 'bg-green-100' : 'bg-red-100'
            }`}>
              <Users className={`w-6 h-6 ${
                modelStatus?.income_model_loaded ? 'text-green-600' : 'text-red-600'
              }`} />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Income Classifier</h3>
              <p className={`text-sm ${
                modelStatus?.income_model_loaded ? 'text-green-600' : 'text-red-600'
              }`}>
                {modelStatus?.income_model_loaded ? 'Model Loaded' : 'Model Not Available'}
              </p>
            </div>
          </div>
          {modelStatus?.income_model_loaded && (
            <div className="text-sm text-gray-600">
              <p>Path: <span className="font-mono text-xs">{modelStatus.income_model_path}</span></p>
            </div>
          )}
        </div>

        <div className="card">
          <div className="flex items-center space-x-4 mb-4">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
              modelStatus?.salary_model_loaded ? 'bg-green-100' : 'bg-red-100'
            }`}>
              <DollarSign className={`w-6 h-6 ${
                modelStatus?.salary_model_loaded ? 'text-green-600' : 'text-red-600'
              }`} />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Salary Regressor</h3>
              <p className={`text-sm ${
                modelStatus?.salary_model_loaded ? 'text-green-600' : 'text-red-600'
              }`}>
                {modelStatus?.salary_model_loaded ? 'Model Loaded' : 'Model Not Available'}
              </p>
            </div>
          </div>
          {modelStatus?.salary_model_loaded && (
            <div className="text-sm text-gray-600">
              <p>Path: <span className="font-mono text-xs">{modelStatus.salary_model_path}</span></p>
            </div>
          )}
        </div>
      </div>

      {/* Feature Importance */}
      <div className="grid lg:grid-cols-2 gap-8 mb-10">
        {modelStatus?.income_model_loaded && incomeFeatures && (
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-teal-500 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900">Income Model Features</h3>
                <p className="text-sm text-gray-600">Top 10 most important features</p>
              </div>
            </div>
            {renderFeatureBars(incomeFeatures)}
          </div>
        )}

        {modelStatus?.salary_model_loaded && salaryFeatures && (
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900">Salary Model Features</h3>
                <p className="text-sm text-gray-600">Top 10 most important features</p>
              </div>
            </div>
            {renderFeatureBars(salaryFeatures)}
          </div>
        )}
      </div>

      {/* How It Works */}
      <div className="card mb-10">
        <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
          <BarChart3 className="w-6 h-6 mr-2 text-blue-600" />
          How Our ML Models Work
        </h3>
        
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <Users className="w-5 h-5 mr-2 text-green-600" />
              Income Classification Model
            </h4>
            <ul className="space-y-2 text-gray-600">
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Trained on the Adult Income Dataset (UCI Machine Learning Repository)</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Uses Logistic Regression, Decision Tree, and Random Forest algorithms</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Automatically selects the best performing model based on F1-score</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Evaluated using Accuracy, Precision, Recall, and F1-score metrics</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Features include age, education, occupation, work hours, and demographics</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <DollarSign className="w-5 h-5 mr-2 text-blue-600" />
              Salary Regression Model
            </h4>
            <ul className="space-y-2 text-gray-600">
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Trained on comprehensive job market data with salary information</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Uses Linear Regression, Decision Tree, and Random Forest regressors</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Selects best model based on R² score and lowest RMSE</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Evaluated using MAE, RMSE, and R² Score metrics</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span>Features include job title, experience, skills, industry, and location</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Dashboard Link */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-center text-white">
        <h3 className="text-2xl font-bold mb-3">Want Deeper Insights?</h3>
        <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
          Run the Streamlit dashboard for interactive visualizations, data exploration, 
          and comprehensive analytics on job market trends.
        </p>
        <code className="bg-white/20 px-4 py-2 rounded-lg font-mono text-sm">
          streamlit run dashboard/dashboard.py
        </code>
      </div>
    </div>
  );
};

export default Insights;
