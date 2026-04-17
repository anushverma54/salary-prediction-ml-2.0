import React, { useState } from 'react';
import { DollarSign, Loader2, CheckCircle, AlertCircle, TrendingUp, Briefcase, RefreshCw } from 'lucide-react';
import { predictSalary } from '../services/api';

const SalaryPrediction = () => {
  const [formData, setFormData] = useState({
    job_title: 'Software Engineer',
    experience_years: 5,
    education_level: 'Bachelor',
    skills_count: 8,
    industry: 'Technology',
    company_size: 'Medium (201-1000)',
    location: 'San Francisco',
    remote_work: 'Hybrid',
    certifications: 'None'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const jobTitles = [
    'Software Engineer', 'Data Scientist', 'Product Manager', 'DevOps Engineer',
    'UI/UX Designer', 'Marketing Manager', 'Sales Representative', 'HR Manager',
    'Business Analyst', 'System Administrator', 'QA Engineer', 'Data Analyst',
    'Full Stack Developer', 'Frontend Developer', 'Backend Developer', 'ML Engineer'
  ];

  const educationLevels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD', 'MBA'];

  const industries = [
    'Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing', 'Education',
    'Consulting', 'Media', 'Government', 'Energy'
  ];

  const companySizes = ['Startup (1-50)', 'Small (51-200)', 'Medium (201-1000)', 'Large (1000+)'];

  const locations = [
    'San Francisco', 'New York', 'Seattle', 'Austin', 'Boston', 'Chicago', 'Denver',
    'Remote', 'Los Angeles', 'Washington DC', 'Atlanta', 'Dallas'
  ];

  const remoteOptions = ['Fully Remote', 'Hybrid', 'On-site'];

  const certifications = [
    'None', 'AWS Certified', 'Google Cloud', 'Azure Certified', 'PMP',
    'Scrum Master', 'Data Science Cert', 'Cybersecurity Cert', 'Multiple'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'experience_years' || name === 'skills_count' ? parseFloat(value) || '' : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictSalary(formData);
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
      job_title: 'Software Engineer',
      experience_years: 5,
      education_level: 'Bachelor',
      skills_count: 8,
      industry: 'Technology',
      company_size: 'Medium (201-1000)',
      location: 'San Francisco',
      remote_work: 'Hybrid',
      certifications: 'None'
    });
  };

  const formatSalary = (salary) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(salary);
  };

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl mb-4">
          <DollarSign className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Exact Salary Prediction</h1>
        <p className="text-gray-600">Get a precise salary estimate based on your profile</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
        {/* Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Briefcase className="w-5 h-5 mr-2 text-blue-600" />
            Job Profile Details
          </h2>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
                <select name="job_title" value={formData.job_title} onChange={handleChange} className="select-field">
                  {jobTitles.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                <select name="industry" value={formData.industry} onChange={handleChange} className="select-field">
                  {industries.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Experience (Years)</label>
                <input
                  type="number"
                  name="experience_years"
                  value={formData.experience_years}
                  onChange={handleChange}
                  required
                  min="0"
                  max="50"
                  step="0.5"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Skills Count</label>
                <input
                  type="number"
                  name="skills_count"
                  value={formData.skills_count}
                  onChange={handleChange}
                  required
                  min="0"
                  max="50"
                  className="input-field"
                />
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Education Level</label>
                <select name="education_level" value={formData.education_level} onChange={handleChange} className="select-field">
                  {educationLevels.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Company Size</label>
                <select name="company_size" value={formData.company_size} onChange={handleChange} className="select-field">
                  {companySizes.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                <select name="location" value={formData.location} onChange={handleChange} className="select-field">
                  {locations.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Remote Work</label>
                <select name="remote_work" value={formData.remote_work} onChange={handleChange} className="select-field">
                  {remoteOptions.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Certifications</label>
              <select name="certifications" value={formData.certifications} onChange={handleChange} className="select-field">
                {certifications.map(opt => <option key={opt} value={opt}>{opt}</option>)}
              </select>
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
                    <span>Predict Salary</span>
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
              <div className="prediction-card bg-gradient-to-r from-blue-500 to-purple-600">
                <div className="flex items-center space-x-3 mb-4">
                  <CheckCircle className="w-8 h-8" />
                  <h3 className="text-2xl font-bold">Predicted Salary</h3>
                </div>
                <div className="text-center py-6">
                  <div className="text-5xl font-bold mb-2">
                    {formatSalary(result.prediction)}
                  </div>
                  <p className="text-blue-100">Estimated Annual Salary</p>
                </div>
                {result.confidence && (
                  <div className="bg-white/20 rounded-lg p-4">
                    <div className="flex justify-between text-sm mb-2">
                      <span>Prediction Confidence</span>
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

              {/* Salary Breakdown */}
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Salary Breakdown</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between py-2 border-b border-gray-100">
                    <span className="text-gray-600">Monthly</span>
                    <span className="font-medium">{formatSalary(result.prediction / 12)}</span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-gray-100">
                    <span className="text-gray-600">Bi-weekly</span>
                    <span className="font-medium">{formatSalary(result.prediction / 26)}</span>
                  </div>
                  <div className="flex justify-between py-2">
                    <span className="text-gray-600">Weekly</span>
                    <span className="font-medium">{formatSalary(result.prediction / 52)}</span>
                  </div>
                </div>
              </div>

              {/* Top Features */}
              {result.top_features && result.top_features.length > 0 && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Influencing Factors</h3>
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
                <DollarSign className="w-10 h-10 text-gray-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Ready to Predict</h3>
              <p className="text-gray-600 max-w-sm">
                Fill in your job details and click "Predict Salary" to see your estimated salary.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SalaryPrediction;
