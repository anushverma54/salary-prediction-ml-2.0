import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import PredictionSelect from './pages/PredictionSelect';
import IncomePrediction from './pages/IncomePrediction';
import SalaryPrediction from './pages/SalaryPrediction';
import Insights from './pages/Insights';
import History from './pages/History';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict" element={<PredictionSelect />} />
            <Route path="/predict/income" element={<IncomePrediction />} />
            <Route path="/predict/salary" element={<SalaryPrediction />} />
            <Route path="/insights" element={<Insights />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
