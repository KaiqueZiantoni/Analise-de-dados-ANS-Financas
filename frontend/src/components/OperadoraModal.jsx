import { useEffect, useState } from 'react';
import api from '../services/api';
import styles from './OperadoraModal.module.css';

const OperadoraModal = ({ cnpj, onClose }) => {
  const [detalhes, setDetalhes] = useState(null);
  const [despesas, setDespesas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [resDetalhes, resDespesas] = await Promise.all([
          api.get(`/operadoras/${cnpj}`),
          api.get(`/operadoras/${cnpj}/despesas`)
        ]);

        setDetalhes(resDetalhes.data);
        setDespesas(resDespesas.data);
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false);
      }
    }

    if (cnpj) fetchData();
  }, [cnpj]);

  if (!cnpj) return null;

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <button className={styles.closeButton} onClick={onClose}>×</button>
        
        {loading ? (
          <div style={{ padding: '20px', textAlign: 'center' }}>Carregando dados...</div>
        ) : detalhes ? (
          <>
            <h2 style={{ marginBottom: '15px', color: '#333' }}>{detalhes.razao_social}</h2>
            
            <div className={styles.infoGrid}>
              <p><strong>CNPJ:</strong> {detalhes.cnpj}</p>
              <p><strong>Registro ANS:</strong> {detalhes.registro_ans}</p>
            </div>

            <h3 style={{ marginTop: '20px', fontSize: '1.1rem', borderBottom: '1px solid #eee', paddingBottom: '5px' }}>
              Histórico de Despesas
            </h3>

            <div style={{ maxHeight: '200px', overflowY: 'auto', marginTop: '10px' }}>
              {despesas.length > 0 ? (
                <table style={{ width: '100%', fontSize: '0.9rem', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ background: '#f0f0f0', textAlign: 'left' }}>
                      <th style={{ padding: '8px' }}>Ano</th>
                      <th style={{ padding: '8px' }}>Trimestre</th>
                      <th style={{ padding: '8px' }}>Valor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {despesas.map((item, index) => (
                      <tr key={index} style={{ borderBottom: '1px solid #eee' }}>
                        <td style={{ padding: '8px' }}>{item.ano}</td>
                        <td style={{ padding: '8px' }}>{item.trimestre}º</td>
                        <td style={{ padding: '8px' }}>
                          {Number(item.valor_despesas).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p style={{ color: '#666', fontStyle: 'italic', marginTop: '10px' }}>
                  Nenhuma despesa registrada para esta operadora.
                </p>
              )}
            </div>
          </>
        ) : (
          <p>Erro ao carregar informações.</p>
        )}
      </div>
    </div>
  );
};

export default OperadoraModal;