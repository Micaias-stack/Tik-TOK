import streamlit as st
import time
import random
import requests

# Configuração da página
st.set_page_config(page_title="Bot Mission Master", page_icon="⚽")

# Lista de User-Agents para simular diferentes dispositivos
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

st.title("⚽ Bot de Chutes TikTok")
st.info("Objetivo: Chegar aos 120 para o saque.")

# --- BARRA LATERAL: CONFIGURAÇÕES ---
st.sidebar.header("⚙️ Configurações do Robô")
num_cliques = st.sidebar.number_input("Quantos convites faltam?", 1, 50, 1)
delay = st.sidebar.slider("Delay entre tentativas (seg)", 5, 30, 10)

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Configuração de Rede")
usar_proxy = st.sidebar.checkbox("Usar Proxy?")
tipo_proxy = st.sidebar.selectbox("Tipo de Proxy", ["Rotativa", "Fixa/Estática"], disabled=not usar_proxy)
proxy_url = st.sidebar.text_input("Endereço da Proxy (IP:Porta)", placeholder="ex: 192.168.1.1:8080", disabled=not usar_proxy)

# --- ÁREA PRINCIPAL ---
link_convite = st.text_input("Cole seu link de convite aqui:", placeholder="https://vm.tiktok.com/...")

if st.button("Iniciar Ciclo de Convites 🚀"):
    if not link_convite:
        st.error("Insira o link primeiro!")
    else:
        progresso = st.progress(0)
        log_area = st.empty()
        
        for i in range(num_cliques):
            # 1. Escolhe um dispositivo aleatório
            ua = random.choice(USER_AGENTS)
            
            # 2. Configura a Proxy se estiver ativa
            proxies = None
            if usar_proxy and proxy_url:
                proxies = {"http": f"http://{proxy_url}", "https": f"http://{proxy_url}"}
            
            log_area.code(f"Tentativa {i+1}/{num_cliques}\nSimulando: {ua[:50]}...\nProxy: {'Ativa' if usar_proxy else 'Nenhuma'}")
            
            try:
                # 3. Simula o acesso ao link
                # O streamilit/python faz a requisição "fingindo" ser o navegador
                headers = {'User-Agent': ua}
                response = requests.get(link_convite, headers=headers, proxies=proxies, timeout=10)
                
                if response.status_code == 200:
                    st.toast(f"Tentativa {i+1} enviada!")
                else:
                    st.warning(f"Erro na tentativa {i+1}: Status {response.status_code}")
            
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
                break

            # 4. Espera o tempo definido (essencial para não ser banido)
            time.sleep(delay)
            progresso.progress((i + 1) / num_cliques)
            
        st.success("🤖 Ciclo completo! Verifique se os chutes subiram.")
        st.balloons()

st.markdown("---")
st.warning("⚠️ **Atenção:** Se você usar Proxy Rotativa, o IP mudará automaticamente a cada clique. Se usar Fixa, o TikTok pode bloquear o IP após algumas tentativas.")
