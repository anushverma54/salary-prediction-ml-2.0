import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Income Prediction API
export const predictIncome = async (data) => {
  try {
    const response = await api.post('/predict-income', data);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Salary Prediction API
export const predictSalary = async (data) => {
  try {
    const response = await api.post('/predict-salary', data);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Get Model Status
export const getModelStatus = async () => {
  try {
    const response = await api.get('/model-status');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Get Prediction History
export const getPredictionHistory = async (limit = 100) => {
  try {
    const response = await api.get(`/prediction-history?limit=${limit}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Clear Prediction History
export const clearPredictionHistory = async () => {
  try {
    const response = await api.delete('/prediction-history');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Retrain Model
export const retrainModel = async (modelType) => {
  try {
    const response = await api.post(`/retrain-model?model_type=${modelType}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Get Feature Importance
export const getFeatureImportance = async (modelType) => {
  try {
    const response = await api.get(`/feature-importance/${modelType}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Download Predictions
export const downloadPredictions = async () => {
  try {
    const response = await api.get('/download-predictions');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export default api;
