import streamlit as st
import feedparser
import datetime

# Configuração da Página
st.set_page_config(page_title="Meu Radar de Notícias", layout="wide", page_icon="📰")

# --- LISTA DE FONTES (RSS) ---
# Aqui centralizamos os feeds que correspondem aos seus interesses:
# 1. Google & IA
# 2. Legislativo & Judiciário
# 3. Notícias Regionais (Divinópolis/Centro-Oeste)
FEEDS = {
    "🤖 Google & IA (The Keyword)": "https://blog.google/rss/",
    "⚖️ STF (Notícias)": "https://www.stf.jus.br/portal/rss/noticiasRss.asp",
    "🏛️ Câmara dos Deputados": "https://www.camara.leg.br/noticias/rss",
    "🔺 G1 Centro-Oeste de Minas": "https://g1.globo.com/dynamo/mg/centro-oeste/rss2.xml",
    "👮 Conjur (Jurídico & Político)": "https://www.conjur.com.br/rss.xml"
}

def get_news(feed_url):
    """Lê o feed RSS e retorna uma lista de dicionários com as notícias."""
    news_items = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:8]: # Pega as 8 mais recentes para ser sucinto
            # Tenta pegar a data de publicação, se não tiver, usa a data atual
            published = entry.get("published", datetime.datetime.now().strftime("%a, %d %b %Y"))
            
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "Sem resumo disponível."),
                "date": published
            })
    except Exception as e:
        st.error(f"Erro ao carregar feed: {e}")
    return news_items

# --- INTERFACE (SIDEBAR) ---
st.sidebar.header("Filtros")
st.sidebar.markdown("Selecione as fontes que deseja monitorizar hoje:")

# Cria checkboxes para cada fonte, todas marcadas por padrão
selected_feeds = {name: url for name, url in FEEDS.items() if st.sidebar.checkbox(name, value=True)}

st.sidebar.markdown("---")
st.sidebar.info("ℹ️ Este painel busca dados diretamente das fontes oficiais, sem algoritmos de recomendação.")

# --- INTERFACE (PRINCIPAL) ---
st.title("📰 Radar de Informação Estratégica")
st.markdown(f"*Atualizado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}*")

# Cria abas para organizar o conteúdo visualmente
if selected_feeds:
    tabs = st.tabs(selected_feeds.keys())
    
    for i, (name, url) in enumerate(selected_feeds.items()):
        with tabs[i]:
            st.subheader(f"Últimas atualizações: {name}")
            news = get_news(url)
            
            if news:
                for item in news:
                    with st.expander(f"{item['title']}"):
                        st.caption(f"📅 {item['date']}")
                        # Limpa tags HTML básicas do resumo se necessário, ou exibe direto
                        st.markdown(item['summary'], unsafe_allow_html=True)
                        st.markdown(f"👉 **[Ler matéria completa]({item['link']})**")
            else:
                st.warning("Não foi possível carregar as notícias desta fonte no momento.")
else:
    st.write("👈 Selecione pelo menos uma fonte na barra lateral.")

