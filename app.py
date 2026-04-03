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

# Campos separados para evitar erro de parse e autenticação
proxy_ip = st.sidebar.text_input("IP e Porta", placeholder="ex: 91.123.10.72:6614")
proxy_user = st.sidebar.text_input("Usuário Proxy (opcional)")
proxy_pass = st.sidebar.text_input("Senha Proxy (opcional)", type="password")

# --- ÁREA PRINCIPAL ---
link_convite = st.text_input("Link do Convite:", placeholder="https://vm.tiktok.com/...")

if st.button("Iniciar Simulação Android 🚀"):
    if not link_convite:
        st.error("Insira o link do TikTok primeiro!")
    elif usar_proxy and not proxy_ip:
        st.error("Você ativou a proxy, mas não colocou o IP:Porta!")
    else:
        progresso = st.progress(0)
        status = st.empty()
        
        # Criamos uma sessão para gerenciar melhor os cookies e a conexão
        session = requests.Session()

        for i in range(num_cliques):
            ua = random.choice(ANDROID_AGENTS)
            
            # Montagem da Proxy com tratamento de espaços
            proxies = None
            if usar_proxy:
                p_ip = proxy_ip.strip()
                p_user = proxy_user.strip()
                p_pass = proxy_pass.strip()
                
                if p_user and p_pass:
                    # Formato que resolve o erro 407 (Authentication Required)
                    p_url = f"http://{p_user}:{p_pass}@{p_ip}"
                else:
                    p_url = f"http://{p_ip}"
                
                proxies = {"http": p_url, "https": p_url}

            status.code(f"Tentativa {i+1}/{num_cliques}\nSimulando Android: {ua.split(';')[1]}\nProxy: {'Ativa' if usar_proxy else 'Desativada'}")
            
            try:
                # Headers para simular um navegador real vindo do Google
                headers = {
                    'User-Agent': ua,
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Referer': 'https://www.google.com/',
                    'Connection': 'keep-alive'
                }
                
                # Executa a visita ao link com a sessão e a proxy configurada
                response = session.get(
                    link_convite, 
                    headers=headers, 
                    proxies=proxies, 
                    timeout=20,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    st.toast(f"✅ Rodada {i+1} concluída!")
                elif response.status_code == 407:
                    st.error("❌ Erro 407: Usuário ou Senha da Proxy estão incorretos!")
                    break
                else:
                    st.warning(f"⚠️ Resposta inesperada: {response.status_code}")
            
            except Exception as e:
                # Trata erros de conexão de forma amigável
                if "407" in str(e):
                    st.error("❌ Erro de Autenticação na Proxy. Verifique Usuário/Senha.")
                else:
                    st.error(f"❌ Erro na Conexão: {str(e)}")
                break

            # Espera o tempo definido para não ser bloqueado rápido
            time.sleep(delay)
            progresso.progress((i + 1) / num_cliques)
            
        st.success("🤖 Ciclo finalizado! Verifique seu app do TikTok.")
        st.balloons()
