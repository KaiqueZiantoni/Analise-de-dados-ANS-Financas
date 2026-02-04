from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine("postgresql://postgres:SuaSenha123@localhost:5432/postgres")

@app.get("/api/operadoras")
def get_operadoras(page: int = 1, limit: int = 10, search: str = Query(None)):
    offset = (page - 1) * limit
    
    params = {"limit": limit, "offset": offset}
    
    where_clause = ""
    if search:
        where_clause = "WHERE razao_social ILIKE :search OR cnpj ILIKE :search"
        params["search"] = f"%{search}%" # O % serve para buscar "contendo" o termo

    query = text(f"""
        SELECT registro_ans, razao_social, cnpj 
        FROM public.operadoras_cadastro 
        {where_clause}
        ORDER BY registro_ans 
        LIMIT :limit OFFSET :offset
    """)
    
    df = pd.read_sql(query, engine, params=params)
    

    total_query = text(f"SELECT COUNT(*) FROM public.operadoras_cadastro {where_clause}")
    total = pd.read_sql(total_query, engine, params=params).iloc[0, 0]
    
    return {
        "data": df.to_dict(orient="records"),
        "total": int(total),
        "page": page,
        "limit": limit
    }

@app.get("/api/operadoras/{cnpj}") 
def get_operadora_detalhe(cnpj: str):
    query = text("SELECT * FROM public.operadoras_cadastro WHERE cnpj = :cnpj")
    df = pd.read_sql(query, engine, params={"cnpj": cnpj})
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
        
    return df.iloc[0].to_dict()

@app.get("/api/operadoras/{cnpj}/despesas")
def get_operadora_despesas(cnpj: str):
    query = text("""
        SELECT d.ano, d.trimestre, d.valor_despesas
        FROM public.despesas_consolidadas d
        JOIN public.operadoras_cadastro o ON d.registro_ans = o.registro_ans
        WHERE o.cnpj = :cnpj
        ORDER BY d.ano DESC, d.trimestre DESC
    """)
    df = pd.read_sql(query, engine, params={"cnpj": cnpj})
    return df.to_dict(orient="records")

@app.get("/api/estatisticas")
def get_estatisticas():
    query_media = "SELECT AVG(valor_despesas) as media_geral FROM public.despesas_consolidadas"
    media = pd.read_sql(query_media, engine).iloc[0, 0]


    query_top5 = """
        SELECT o.razao_social, SUM(d.valor_despesas) as total
        FROM public.despesas_consolidadas d
        JOIN public.operadoras_cadastro o ON d.registro_ans = o.registro_ans
        GROUP BY o.razao_social
        ORDER BY total DESC
        LIMIT 5
    """
    top5 = pd.read_sql(query_top5, engine).to_dict(orient="records")
    
    return {
        "media_trimestral_geral": media,
        "top_5_operadoras": top5
    }