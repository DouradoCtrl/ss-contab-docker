import streamlit as st
import pandas as pd
from sqlalchemy import text

def render_filtros(conn):
	# Buscar clientes do banco
	clientes_df = conn.query('SELECT id, nome FROM clientes ORDER BY nome;')

	with st.expander('Filtros', expanded=False):
		# Cliente em destaque
		clientes = [(row['nome'], row['id']) for _, row in clientes_df.iterrows()] if not clientes_df.empty else []
		cliente_nome_id = st.selectbox('Cliente', options=[('Todos', None)] + clientes, format_func=lambda x: x[0], index=0)
		cliente, cliente_id = cliente_nome_id

		# Linha com mês e ano juntos
		col1, col2, col3, col4 = st.columns(4)
		with col1:
			mes = st.selectbox(
				'Mês',
				options=[
					'Todos', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
					'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
				],
				index=0
			)
		with col2:
			from datetime import datetime
			ano_atual = datetime.now().year
			anos = [str(a) for a in range(2025, ano_atual + 1)]
			ano = st.selectbox(
				'Ano',
				options=anos,
				index=len(anos)-1
			)
		with col3:
			data_inicio = st.date_input('Data início', value=None, key='data_inicio')
		with col4:
			data_fim = st.date_input('Data fim', value=None, key='data_fim')

		return {
			'mes': mes,
			'ano': ano,
			'data_inicio': data_inicio,
			'data_fim': data_fim,
			'cliente': cliente,
			'cliente_id': cliente_id
		}
