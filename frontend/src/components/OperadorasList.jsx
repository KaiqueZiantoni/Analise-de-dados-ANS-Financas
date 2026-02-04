import { useState, useEffect } from 'react';
import api from '../services/api';
import styles from './OperadorasList.module.css';
import OperadoraModal from './OperadoraModal';

const OperadorasList = () => {
  const [operadoras, setOperadoras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [selectedCnpj, setSelectedCnpj] = useState(null);
  
  const [busca, setBusca] = useState(''); 

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {

        const response = await api.get('/operadoras', {
          params: { 
            page: page, 
            limit: 10,
            search: busca 
          }
        });
        setOperadoras(response.data.data);
        setTotal(response.data.total);
      } catch (error) {
        console.error("Erro:", error);
      } finally {
        setLoading(false);
      }
    };

    const delayDebounce = setTimeout(() => {
      loadData();
    }, 500);

    return () => clearTimeout(delayDebounce);

  }, [page, busca]); 

  const handleSearch = (e) => {
    setBusca(e.target.value);
    setPage(1); 
  };

  const handleNext = () => setPage(page + 1);
  const handlePrev = () => setPage(page - 1);

  return (
    <div className={styles.container}>
      <h2>Operadoras Ativas</h2>

      {/* 3. Campo de Busca */}
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Buscar por Razão Social ou CNPJ..."
          value={busca}
          onChange={handleSearch}
          style={{
            padding: '10px',
            width: '100%',
            maxWidth: '400px',
            borderRadius: '5px',
            border: '1px solid #ccc',
            fontSize: '1rem'
          }}
        />
      </div>
      
      {loading ? (
         <p>Carregando...</p>
      ) : (
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Registro ANS</th>
              <th>CNPJ</th>
              <th>Razão Social</th>
              <th style={{textAlign: 'center'}}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {operadoras.length > 0 ? (
              operadoras.map((op) => (
                <tr key={op.registro_ans}>
                  <td>{op.registro_ans}</td>
                  <td>{op.cnpj}</td>
                  <td>{op.razao_social}</td>
                  <td style={{textAlign: 'center'}}>
                    <button 
                      className={styles.button}
                      onClick={() => setSelectedCnpj(op.cnpj)}
                    >
                      Ver Detalhes
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" style={{textAlign: 'center', padding: '20px'}}>
                  Nenhuma operadora encontrada.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}

      <div className={styles.actions}>
         <button className={styles.button} onClick={handlePrev} disabled={page === 1}>Anterior</button>
         <span>Página {page}</span>
         <button className={styles.button} onClick={handleNext} disabled={page * 10 >= total}>Próxima</button>
      </div>

      {selectedCnpj && (
        <OperadoraModal 
          cnpj={selectedCnpj} 
          onClose={() => setSelectedCnpj(null)} 
        />
      )}
    </div>
  );
};

export default OperadorasList;