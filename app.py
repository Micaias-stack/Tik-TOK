import streamlit as st
import time
import random
import requests

st.set_page_config(page_title="Bot Mission Android", page_icon="⚽")

ANDROID_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
]

st.title("⚽ Bot de Chutes (V3)")

st.sidebar.header("⚙️ Configurações")
num_cliques = st.sidebar.number_input("Quantos convites?", 1, 100, 5)
delay = st.sidebar.slider("Delay (segundos)", 5, 60, 10)

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Configuração de Proxy")
usar_proxy = st.sidebar.checkbox("Ativar Proxy")
proxy_ip = st.sidebar.text_input("IP e Porta", value="91.123.10.233:6775")
proxy_user = st.sidebar.text_input("Usuário Proxy", value="flashproxys718")
proxy_pass = st.sidebar.text_input("Senha Proxy", value="nosindique777", type="password")

link_convite = st.text_input("Link do Convite:", placeholder="https://vm.tiktok.com/...")

if st.button("Iniciar Simulação 🚀"):
    if not link_convite:
        st.error("Insira o link!")
    else:
        progresso = st.progress(0)
        status = st.empty()
        
        for i in range(num_cliques):
            ua = random.choice(ANDROID_AGENTS)
            proxies = None
            
            if usar_proxy:
                # Tentando forçar o protocolo HTTP e SOCKS5 se disponível
                auth = f"{proxy_user.strip()}:{proxy_pass.strip()}"
                ip_p = proxy_ip.strip()
                p_url = f"http://{auth}@{ip_p}"
                proxies = {"http": p_url, "https": p_url}

            status.code(f"Rodada {i+1} - Tentando Conexão...")
            
            try:
                # Timeout maior para dar tempo da proxy responder
                headers = {'User-Agent': ua, 'Accept-Language': 'pt-BR,pt;q=0.9'}
                r = requests.get(link_convite, headers=headers, proxies=proxies, timeout=25)
                
                if r.status_code == 200:
                    st.toast(f"✅ Sucesso na tentativa {i+1}!")
                else:
                    st.warning(f"Atenção: Código {r.status_code}")
            
            except Exception as e:
                # Se der erro 407 aqui, é bloqueio do fornecedor da proxy
                st.error(f"Erro Crítico: {str(e)}")
                if "407" in str(e):
                    st.info("💡 Dica: Verifique no SITE da sua proxy se você precisa liberar o IP ou se o plano expirou.")
                break

            time.sleep(delay)
            progresso.progress((i + 1) / num_cliques)
        st.success("Fim do ciclo.")
