import { Routes, Route, Navigate } from 'react-router-dom'
import Connexion from './pages/Connexion'
import Inscription from './pages/Inscription'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/connexion" replace />} />
      <Route path="/connexion" element={<Connexion />} />
      <Route path="/inscription" element={<Inscription />} />
    </Routes>
  )
}

export default App
