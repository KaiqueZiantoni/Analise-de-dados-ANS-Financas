import OperadorasList from './components/OperadorasList';
import DashboardChart from './components/DashboardChart';

function App() {
  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '30px', color: '#333' }}>
        Dashboard ANS
      </h1>
      
      <DashboardChart />

      <OperadorasList />
    </div>
  )
}

export default App;