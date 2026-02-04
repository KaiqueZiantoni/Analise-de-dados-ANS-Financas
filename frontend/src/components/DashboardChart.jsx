import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import api from '../services/api';

const DashboardChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    api.get('/estatisticas')
      .then(response => {
        setData(response.data.top_5_operadoras || []); 
      })
      .catch(error => console.error("Erro ao carregar gráfico", error));
  }, []);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      notation: "compact",
      compactDisplay: "short",
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatName = (name) => {
    if (name.length > 15) {
      return name.substring(0, 15) + '...';
    }
    return name;
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ background: '#fff', border: '1px solid #ccc', padding: '10px', borderRadius: '5px', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
          <p style={{ fontWeight: 'bold', margin: 0, fontSize: '0.9rem' }}>{label}</p>
          <p style={{ margin: 0, color: '#007bff', fontSize: '0.9rem' }}>
            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(payload[0].value)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ 
      background: 'white', 
      padding: '20px', 
      borderRadius: '8px', 
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      marginBottom: '30px',
      height: '400px'
    }}>
      <h3>Top 5 Operadoras com Maiores Despesas</h3>
      
      {data.length > 0 ? (
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            
            <XAxis 
              dataKey="razao_social" 
              tickFormatter={formatName} 
              interval={0}
              tick={{ fontSize: 12 }}
            />
            
            <YAxis 
              tickFormatter={formatCurrency}
              width={80}
              tick={{ fontSize: 12 }}
            />
            
            
            <Tooltip 
              content={<CustomTooltip />} 
              cursor={{ fill: 'transparent' }} 
            />
            
            <Bar dataKey="total" fill="#007bff" barSize={60} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <p style={{textAlign: 'center', marginTop: '50px', color: '#666'}}>
          Carregando dados do gráfico...
        </p>
      )}
    </div>
  );
};

export default DashboardChart;