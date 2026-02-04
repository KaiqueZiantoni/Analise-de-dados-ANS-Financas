
-- QUERY 1 --

WITH periodos AS (
    SELECT 
        MIN(trimestre) as primeiro_tri, 
        MAX(trimestre) as ultimo_tri,
        ano
    FROM public.despesas_consolidadas
    GROUP BY ano
    LIMIT 1
),
q_inicial AS (
    SELECT dc.registro_ans, dc.valor_despesas AS valor_inicial
    FROM public.despesas_consolidadas dc, periodos p
    WHERE dc.trimestre = p.primeiro_tri AND dc.ano = p.ano
),
q_final AS (
    SELECT dc.registro_ans, dc.valor_despesas AS valor_final
    FROM public.despesas_consolidadas dc, periodos p
    WHERE dc.trimestre = p.ultimo_tri AND dc.ano = p.ano
)
SELECT 
    op.razao_social, 
    qi.registro_ans,
    qi.valor_inicial,
    qf.valor_final,
    ((qf.valor_final - qi.valor_inicial) / NULLIF(qi.valor_inicial, 0)) * 100 AS crescimento_percentual
FROM q_inicial qi
INNER JOIN q_final qf ON qi.registro_ans = qf.registro_ans
JOIN public.operadoras_cadastro op ON qi.registro_ans = op.registro_ans
WHERE qi.valor_inicial > 0 
ORDER BY crescimento_percentual DESC
LIMIT 5;

--QUERY 2 --

SELECT 
    op.uf,
    op.razao_social, 
    SUM(dc.valor_despesas) AS despesa_total_operadora_na_uf,
    AVG(dc.valor_despesas) AS media_despesa_por_operadora
FROM public.despesas_consolidadas dc
JOIN public.operadoras_cadastro op ON dc.registro_ans = op.registro_ans
GROUP BY op.uf, op.razao_social 
ORDER BY despesa_total_operadora_na_uf DESC
LIMIT 5;


--QUERY 3 --
WITH media_global AS (
    SELECT AVG(valor_despesas) AS valor_medio_geral 
    FROM public.despesas_consolidadas
),
contagem_acima AS (
    SELECT 
        dc.registro_ans,
        COUNT(*) AS trimestres_acima
    FROM public.despesas_consolidadas dc, media_global mg
    WHERE dc.valor_despesas > mg.valor_medio_geral
    GROUP BY dc.registro_ans
)
SELECT 
    op.razao_social, 
    ca.registro_ans, 
    ca.trimestres_acima
FROM contagem_acima ca
JOIN public.operadoras_cadastro op ON ca.registro_ans = op.registro_ans
WHERE ca.trimestres_acima >= 2
ORDER BY ca.trimestres_acima DESC;