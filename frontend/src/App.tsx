/**
 * Main App component with routing
 */
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Briefings from './pages/Briefings';
import BriefingDetail from './pages/BriefingDetail';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/briefings" element={<Briefings />} />
          <Route path="/briefings/:slug" element={<BriefingDetail />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
