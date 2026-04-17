import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, TrendingUp, BarChart3, ArrowRight, Sparkles, Target, Shield } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Predictions',
      description: 'Machine learning models trained on thousands of data points to deliver accurate salary and income predictions.'
    },
    {
      icon: TrendingUp,
      title: 'Market Insights',
      description: 'Comprehensive analytics dashboard showing job market trends, salary distributions, and career insights.'
    },
    {
      icon: BarChart3,
      title: 'Feature Analysis',
      description: 'Understand which factors most influence your earning potential with detailed feature importance analysis.'
    },
    {
      icon: Target,
      title: 'Dual Prediction Engine',
      description: 'Both classification (>50K or <=50K) and exact salary regression models for comprehensive analysis.'
    },
    {
      icon: Shield,
      title: 'Production Ready',
      description: 'Built with FastAPI and React, featuring modular architecture ready for deployment.'
    },
    {
      icon: Sparkles,
      title: 'Interactive Dashboard',
      description: 'Beautiful Streamlit dashboard with Plotly visualizations for deep data exploration.'
    }
  ];

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="text-center py-16 lg:py-24">
        <div className="inline-flex items-center space-x-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
          <Sparkles className="w-4 h-4" />
          <span>Powered by Machine Learning</span>
        </div>
        
        <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
          Smart Salary Predictor &<br />
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Job Market Insights
          </span>
        </h1>
        
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10">
          Predict your earning potential with AI-powered machine learning models.
          Get insights into job market trends and understand what drives salary growth.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <Link to="/predict" className="btn-primary flex items-center space-x-2">
            <Brain className="w-5 h-5" />
            <span>Start Prediction</span>
          </Link>
          <Link to="/insights" className="btn-secondary flex items-center space-x-2">
            <BarChart3 className="w-5 h-5" />
            <span>View Insights</span>
          </Link>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 border-y border-gray-200">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold text-blue-600 mb-2">2</div>
            <div className="text-gray-600">ML Models</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-purple-600 mb-2">15K+</div>
            <div className="text-gray-600">Training Samples</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-600 mb-2">95%</div>
            <div className="text-gray-600">Accuracy</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-orange-600 mb-2">Real-time</div>
            <div className="text-gray-600">Predictions</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Key Features</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Everything you need to understand salary trends and predict earning potential
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="card hover:shadow-lg transition-shadow duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center mb-4">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 lg:p-12 text-center text-white">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">Ready to Predict Your Salary?</h2>
          <p className="text-blue-100 text-lg mb-8 max-w-2xl mx-auto">
            Try our dual prediction engines - classify your income level or predict your exact salary based on your profile.
          </p>
          <Link 
            to="/predict" 
            className="inline-flex items-center space-x-2 bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold hover:bg-blue-50 transition-colors duration-200"
          >
            <span>Get Started Now</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
