import streamlit as st
from scipy.stats import binom

# Função que encontra o plano amostral com base nos inputs fornecidos
def encontrar_plano_amostral(TAMANHO_LOTE, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX):
    progresso = st.progress(0)  # Barra de progresso
    status_text = st.empty()    # Texto de status
    for tamanho_amostra in range(1, TAMANHO_LOTE + 1):
        for aceitacao_maxima in range(tamanho_amostra + 1):
            risco_fornecedor = 1 - binom.cdf(aceitacao_maxima, tamanho_amostra, NQA)
            risco_consumidor = binom.cdf(aceitacao_maxima, tamanho_amostra, PTDL)
            progresso.progress(tamanho_amostra / TAMANHO_LOTE)  # Atualiza barra de progresso
            status_text.text(f'Calculando: {tamanho_amostra}/{TAMANHO_LOTE} amostras, aceitação máxima: {aceitacao_maxima}')
            if risco_fornecedor <= RISCO_FORNECEDOR_MAX and risco_consumidor <= RISCO_CONSUMIDOR_MAX:
                return tamanho_amostra, aceitacao_maxima, risco_fornecedor, risco_consumidor
    return None, None, None, None

# Interface do Streamlit
st.title('Plano Amostral')

# Entradas dos parâmetros
TAMANHO_LOTE = st.number_input('Tamanho do Lote:', min_value=1, value=10000, step=1)
NQA = st.number_input('NQA:', min_value=0.0, value=0.02, step=0.01, format="%.3f")
PTDL = st.number_input('PTDL:', min_value=0.0, value=0.04, step=0.01, format="%.3f")
RISCO_FORNECEDOR_MAX = st.number_input('Risco Fornec. Máx:', min_value=0.0, value=0.100, step=0.01, format="%.3f")
RISCO_CONSUMIDOR_MAX = st.number_input('Risco Cons. Máx:', min_value=0.0, value=0.075, step=0.01, format="%.3f")

# Botão para calcular o plano amostral
if st.button('Calcular Plano Amostral'):
    tamanho_amostra, aceitacao_maxima, risco_fornecedor, risco_consumidor = encontrar_plano_amostral(
        TAMANHO_LOTE, NQA, PTDL, RISCO_FORNECEDOR_MAX, RISCO_CONSUMIDOR_MAX
    )
    
    if tamanho_amostra is not None:
        st.write(f'Tamanho da amostra: {tamanho_amostra}')
        st.write(f'Índice de aceitação máxima: {aceitacao_maxima}')
        st.write(f'Risco do fornecedor: {risco_fornecedor:.3f}')
        st.write(f'Risco do consumidor: {risco_consumidor:.3f}')
    else:
        st.write('Nenhum plano amostral encontrado com os parâmetros fornecidos.')
