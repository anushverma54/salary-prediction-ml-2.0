import React, { useState } from 'react';
import { Users, Loader2, CheckCircle, AlertCircle, TrendingUp, BarChart3, RefreshCw } from 'lucide-react';
import { predictIncome } from '../services/api';

const IncomePrediction = () => {
  const [formData, setFormData] = useState({
    age: '',
    education: 'Bachelors',
    occupation: 'Tech-support',
    workclass: 'Private',
    gender: 'Male',
    marital_status: 'Never-married',
    hours_per_week: 40,
    native_country: 'United-States'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const educationOptions = [
    'Preschool', '1st-4th', '5th-6th', '7th-8th', '9th', '10th', '11th', '12th',
    'HS-grad', 'Some-college', 'Assoc-voc', 'Assoc-acdm', 'Bachelors', 'Masters',
    'Prof-school', 'Doctorate'
  ];

  const occupationOptions = [
    'Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial',
    'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical',
    'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'
  ];

  const workclassOptions = [
    'Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov',
    'State-gov', 'Without-pay', 'Never-worked'
  ];

  const maritalOptions = [
    'Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed',
    'Married-spouse-absent', 'Married-AF-spouse'
  ];

  const countryOptions = [
    'United-States', 'Cuba', 'Jamaica', 'India', 'Mexico', 'South', 'Puerto-Rico',
    'Honduras', 'England', 'Canada', 'Germany', 'Iran', 'Philippines', 'Italy',
    'Poland', 'Columbia', 'Cambodia', 'Thailand', 'Ecuador', 'Laos', 'Taiwan',
    'Haiti', 'Portugal', 'Dominican-Republic', 'El-Salvador', 'France', 'Guatemala',
    'China', 'Japan', 'Yugoslavia', 'Peru', 'Outlying-US(Guam-USVI-etc)', 'Scotland',
    'Trinadad&Tobago', 'Greece', 'Nicaragua', 'Vietnam', 'Hong', 'Ireland', 'Hungary',
    'Holand-Netherlands'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'age' || name === 'hours_per_week' ? parseInt(value) || '' : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictIncome(formData);
      setResult(data);
    } catch (err) {
      setError(err.detail || 'Failed to make prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setFormData({
      age: '',
      education: 'Bachelors',
      occupation: 'Tech-support',
      workclass: 'Private',
      gender: 'Male',
      marital_status: 'Never-married',
      hours_per_week: 40,
      native_country: 'United-States'
    });
  };

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-teal-500 rounded-2xl mb-4">
          <Users className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Income Classification</h1>
        <p className="text-gray-600">Predict whether your income will be greater than $50K</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
        {/* Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <BarChart3 className="w-5 h-5 mr-2 text-blue-600" />
            Enter Your Details
          </h2>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  required
                  min="18"
                  max="100"
                  className="input-field"
                  placeholder="e.g., 30"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Hours per Week</label>
                <input
                  type="number"
                  name="hours_per_week"
                  value={formData.hours_per_week}
                  onChange={handleChange}
                  required
                  min="1"
                  max="100"
                  className="input-field"
                />
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Education</label>
                <select name="education" value={formData.education} onChange={handleChange} className="select-field">
                  {educationOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Occupation</label>
                <select name="occupation" value={formData.occupation} onChange={handleChange} className="select-field">
                  {occupationOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Work Class</label>
                <select name="workclass" value={formData.workclass} onChange={handleChange} className="select-field">
                  {workclassOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Marital Status</label>
                <select name="marital_status" value={formData.marital_status} onChange={handleChange} className="select-field">
                  {maritalOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                <select name="gender" value={formData.gender} onChange={handleChange} className="select-field">
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Native Country</label>
                <select name="native_country" value={formData.native_country} onChange={handleChange} className="select-field">
                  {countryOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>
            </div>

            <div className="pt-4 flex space-x-4">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 btn-primary flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Predicting...</span>
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-5 h-5" />
                    <span>Predict Income</span>
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="btn-secondary"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2 text-red-700">
              <AlertCircle className="w-5 h-5" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Results */}
        <div>
          {result ? (
            <div className="space-y-6 animate-slide-up">
              {/* Prediction Card */}
              <div className="prediction-card">
                <div className="flex items-center space-x-3 mb-4">
                  <CheckCircle className="w-8 h-8" />
                  <h3 className="text-2xl font-bold">Prediction Result</h3>
                </div>
                <div className="text-center py-6">
                  <div className="text-5xl font-bold mb-2">
                    {result.prediction}
                  </div>
                  <p className="text-blue-100">Predicted Income Class</p>
                </div>
                {result.confidence && (
                  <div className="bg-white/20 rounded-lg p-4">
                    <div className="flex justify-between text-sm mb-2">
                      <span>Confidence</span>
                      <span className="font-semibold">{(result.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div className="feature-bar bg-white/30">
                      <div 
                        className="feature-bar-fill bg-white"
                        style={{ width: `${result.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Top Features */}
              {result.top_features && result.top_features.length > 0 && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Influencing Features</h3>
                  <div className="space-y-4">
                    {result.top_features.map((feature, index) => (
                      <div key={index}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-700">{feature.feature}</span>
                          <span className="text-gray-500">{(feature.importance * 100).toFixed(1)}%</span>
                        </div>
                        <div className="feature-bar">
                          <div 
                            className="feature-bar-fill"
                            style={{ width: `${feature.importance * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Model Info */}
              <div className="card bg-gray-50">
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Model Used:</span>
                  <span className="font-medium text-gray-900">{result.model_used}</span>
                </div>
                <div className="flex justify-between text-sm text-gray-600 mt-2">
                  <span>Timestamp:</span>
                  <span className="font-medium text-gray-900">
                    {new Date(result.timestamp).toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div className="card h-full flex flex-col items-center justify-center text-center py-16">
              <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <BarChart3 className="w-10 h-10 text-gray-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Ready to Predict</h3>
              <p className="text-gray-600 max-w-sm">
                Fill in your details and click "Predict Income" to see the classification result.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default IncomePrediction;
