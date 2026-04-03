import streamlit as st
import time
import random
import requests

# Configuração da página
st.set_page_config(page_title="Bot Mission Android", page_icon="⚽")

# Lista focada apenas em ANDROID (Marcas diferentes) para simular usuários inativos
ANDROID_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Samsung S21
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.036) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Pixel 6
    "Mozilla/5.0 (Linux; Android 11; M2007J20CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Xiaomi POCO
    "Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", # Samsung A50
    "Mozilla/5.0 (Linux; Android 13; Motorola Edge 30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36" # Motorola
]

st.title("⚽ Bot de Chutes (Modo Android Inativo)")

# --- BARRA LATERAL ---
st.sidebar.header("⚙️ Configurações")
num_cliques = st.sidebar.number_input("Quantos convites?", 1, 100, 5)
delay = st.sidebar.slider("Delay (segundos)", 5, 60, 15)

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Configuração de Proxy")
usar_proxy = st.sidebar.checkbox("Ativar Proxy")

# Novos campos para resolver o erro "Failed to Parse"
proxy_ip = st.sidebar.text_input("IP e Porta", placeholder="ex: 91.123.10.72:6614")
proxy_user = st.sidebar.text_input("Usuário Proxy (opcional)")
proxy_pass = st.sidebar.text_input("Senha Proxy (opcional)", type="password")

# --- ÁREA PRINCIPAL ---
link_convite = st.text_input("Link do Convite:", placeholder="https://vm.tiktok.com/...")

if st.button("Iniciar Simulação Android 🚀"):
    if not link_convite or (usar_proxy and not proxy_ip):
        st.error("Preencha o link e os dados da Proxy!")
    else:
        progresso = st.progress(0)
        status = st.empty()
        
        for i in range(num_cliques):
            ua = random.choice(ANDROID_AGENTS)
            
            # Montagem correta da URL da Proxy com Autenticação
            proxies = None
            if usar_proxy:
                if proxy_user and proxy_pass:
                    # Formato: http://usuario:senha@ip:porta
                    p_url = f"http://{proxy_user}:{proxy_pass}@{proxy_ip}"
                else:
                    p_url = f"http://{proxy_ip}"
                
                proxies = {"http": p_url, "https": p_url}

            status.code(f"Tentativa {i+1}/{num_cliques}\nSimulando Android: {ua.split(';')[1]}\nStatus: Processando...")
            
            try:
                # Headers extras para parecer mais real
                headers = {
                    'User-Agent': ua,
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Referer': 'https://www.google.com/'
                }
                
                # Faz a visita ao link
                response = requests.get(link_convite, headers=headers, proxies=proxies, timeout=15)
                
                if response.status_code == 200:
                    st.toast(f"Sucesso na rodada {i+1}!")
                else:
                    st.warning(f"Resposta inesperada: {response.status_code}")
            
            except Exception as e:
                st.error(f"Erro na Proxy: {str(e)}")
                break

            time.sleep(delay)
            progresso.progress((i + 1) / num_cliques)
            
        st.success("✅ Ciclo finalizado!")
