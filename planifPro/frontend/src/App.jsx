import { Routes, Route, Navigate } from 'react-router-dom'
import Connexion from './pages/Connexion'
import RouteProtegee from './components/RouteProtegee'
import Inscription from './pages/Inscription'
import DashboardProfesseur from './pages/DashboardProfesseur'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/connexion" replace />} />
      <Route path="/connexion" element={<Connexion />} />
      <Route path="/inscription" element={<Inscription />} />
      <Route 
        path="/dashboard-prof"
        element={
          <RouteProtegee>
            <DashboardProfesseur />
          </RouteProtegee>
        }
      />
    </Routes>
  )
}

export default App
