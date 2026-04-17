import React from 'react';
import { Link } from 'react-router-dom';
import { Users, DollarSign, ArrowRight, Target, BarChart } from 'lucide-react';

const PredictionSelect = () => {
  const options = [
    {
      id: 'income',
      title: 'Income Classification',
      description: 'Predict whether your income will be greater than $50K or less than/equal to $50K based on demographic and employment data.',
      icon: Users,
      features: [
        'Binary classification (>50K vs <=50K)',
        'Based on demographics & occupation',
        'Multiple ML algorithms',
        'Confidence score included'
      ],
      color: 'from-green-500 to-teal-500',
      bgColor: 'bg-green-50',
      path: '/predict/income'
    },
    {
      id: 'salary',
      title: 'Exact Salary Prediction',
      description: 'Get a precise salary estimate in dollars based on your job details, experience, skills, and industry factors.',
      icon: DollarSign,
      features: [
        'Numeric salary prediction',
        'Job-specific factors',
        'Experience & skills weighted',
        'Industry benchmarking'
      ],
      color: 'from-blue-500 to-purple-500',
      bgColor: 'bg-blue-50',
      path: '/predict/salary'
    }
  ];

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Choose Your Prediction Type
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Select the prediction model that best fits your needs. Both models are powered by machine learning.
        </p>
      </div>

      {/* Options Grid */}
      <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        {options.map((option) => {
          const Icon = option.icon;
          return (
            <Link
              key={option.id}
              to={option.path}
              className="group card hover:shadow-xl transition-all duration-300 border-2 border-transparent hover:border-blue-200"
            >
              {/* Icon Header */}
              <div className={`w-16 h-16 bg-gradient-to-r ${option.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                <Icon className="w-8 h-8 text-white" />
              </div>

              {/* Title */}
              <h2 className="text-2xl font-bold text-gray-900 mb-3">
                {option.title}
              </h2>

              {/* Description */}
              <p className="text-gray-600 mb-6">
                {option.description}
              </p>

              {/* Features */}
              <ul className="space-y-3 mb-6">
                {option.features.map((feature, index) => (
                  <li key={index} className="flex items-center space-x-2 text-sm text-gray-600">
                    <Target className="w-4 h-4 text-green-500 flex-shrink-0" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA Button */}
              <div className={`flex items-center justify-between ${option.bgColor} rounded-xl p-4 group-hover:bg-opacity-70 transition-colors`}>
                <span className={`font-semibold bg-gradient-to-r ${option.color} bg-clip-text text-transparent`}>
                  Start Prediction
                </span>
                <div className={`w-10 h-10 bg-gradient-to-r ${option.color} rounded-full flex items-center justify-center group-hover:translate-x-1 transition-transform`}>
                  <ArrowRight className="w-5 h-5 text-white" />
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Info Card */}
      <div className="max-w-5xl mx-auto mt-12">
        <div className="card bg-gradient-to-r from-gray-50 to-blue-50 border-blue-100">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <BarChart className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                How It Works
              </h3>
              <p className="text-gray-600">
                Our machine learning models have been trained on thousands of real-world data points. 
                The <strong>Income Classification</strong> model uses demographic and employment data to predict income brackets, 
                while the <strong>Exact Salary Prediction</strong> model estimates specific salary amounts based on job characteristics. 
                Both models provide confidence indicators and feature importance analysis.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionSelect;
