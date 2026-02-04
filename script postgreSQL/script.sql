

CREATE TABLE public.despesas_agregadas_bi (
	id_agregado serial4 NOT NULL,
	registro_ans int4 NULL,
	razao_social varchar(255) NULL,
	uf varchar(2) NULL,
	total_despesas numeric(18, 2) NULL,
	media_trimestral numeric(18, 2) NULL,
	variabilidade_std numeric(18, 2) NULL,
	data_carga date DEFAULT CURRENT_DATE NULL,
	CONSTRAINT despesas_agregadas_bi_pkey PRIMARY KEY (id_agregado)
);

CREATE TABLE public.despesas_consolidadas (
	id_despesa serial4 NOT NULL,
	registro_ans int4 NOT NULL,
	ano int4 NOT NULL,
	trimestre int4 NOT NULL,
	valor_despesas numeric(18, 2) NULL,
	CONSTRAINT despesas_consolidadas_pkey PRIMARY KEY (id_despesa)
);
CREATE INDEX idx_despesas_registro ON public.despesas_consolidadas USING btree (registro_ans);

CREATE TABLE public.operadoras_cadastro (
	registro_ans int4 NOT NULL,
	cnpj varchar(20) NOT NULL,
	razao_social varchar(255) NOT NULL,
	modalidade varchar(100) NULL,
	uf varchar(2) NULL,
	CONSTRAINT operadoras_cadastro_pkey PRIMARY KEY (registro_ans)
);
CREATE INDEX idx_operadora_cnpj ON public.operadoras_cadastro USING btree (cnpj);

ALTER TABLE public.despesas_consolidadas ADD CONSTRAINT fk_operadora_despesa FOREIGN KEY (registro_ans) REFERENCES public.operadoras_cadastro(registro_ans);
