import os
import re
import time
from telethon import TelegramClient, events

# ==========================================
# --- CREDENCIAIS JOTTA SECRETÁRIO ---
# ==========================================
API_ID = 25177007
API_HASH = 'b2a508d67b45bfd330216410168ff654'
GRUPOS_VIP = [-1002477218350, -1002488469430]
LINK_FREE = "https://t.me/O_Arquivista"

# --- CAMINHOS NO TERMUX ---
CAMINHO_BASE = '/data/data/com.termux/files/home/o-arquivista/'
CAMINHO_POSTS = os.path.join(CAMINHO_BASE, 'content/posts/')
CAMINHO_FOTOS = os.path.join(CAMINHO_BASE, 'static/images/projetos/')

# ==========================================
# --- LÓGICA DE TRATAMENTO ---
# ==========================================

client = TelegramClient('sessao_jotta', API_ID, API_HASH)

def formatar_titulo(nome_arquivo):
    """Transforma o nome do arquivo em um título matador para o Google"""
    titulo = re.sub(r'\.(zip|rar|7z|dxf|lbrn2|svg|ai|cdr)', '', nome_arquivo, flags=re.IGNORECASE)
    titulo = titulo.replace('_', ' ').replace('-', ' ').title()
    return f"Projeto Corte Laser {titulo} - Arquivo DXF"

@client.on(events.NewMessage(chats=GRUPOS_VIP))
async def handler(event):
    if event.file and event.file.ext in ['.zip', '.rar', '.7z']:
        print(f"📦 Novo projeto detectado: {event.file.name}")
        
        nome_arq = event.file.name
        titulo_seo = formatar_titulo(nome_arq)
        slug = re.sub(r'\W+', '-', titulo_seo.lower()).strip('-')

        mensagens = await client.get_messages(event.chat_id, limit=10)
        foto_nome = "placeholder.jpg"
        
        for msg in mensagens:
            if msg.photo:
                os.makedirs(CAMINHO_FOTOS, exist_ok=True)
                foto_local = await msg.download_media(file=os.path.join(CAMINHO_FOTOS, f"{slug}.jpg"))
                foto_nome = os.path.basename(foto_local)
                print(f"📸 Foto capturada: {foto_nome}")
                break

        os.makedirs(CAMINHO_POSTS, exist_ok=True)
        post_path = os.path.join(CAMINHO_POSTS, f"{slug}.md")

        # 👇 A MÁGICA MUDA AQUI 👇
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{titulo_seo}"
date: {event.date.isoformat()}
description: "Confira o projeto {titulo_seo} para CNC Laser. Vetores profissionais testados em MDF e Acrílico."
cover:
    image: "/images/projetos/{foto_nome}"
    alt: "{titulo_seo}"
    hiddenInList: false
    hiddenInSingle: false
---

![{titulo_seo}](/images/projetos/{foto_nome})

O projeto **{titulo_seo}** é um dos itens exclusivos que compõem o catálogo de **O Arquivista VIP**. 

Este arquivo foi desenvolvido e testado para garantir a melhor performance em sua máquina laser (MDF, Acrílico ou outros materiais). 

### 🚀 Como acessar este projeto?

Para baixar este arquivo e explorar milhares de outros vetores profissionais, entre no nosso grupo de entrada. Lá você terá informações sobre como acessar o acervo completo e conferir nossos conteúdos gratuitos.

### 📥 [Entrar no Grupo O Arquivista]({LINK_FREE})

*Nota: Este projeto foi postado originalmente em nossa comunidade VIP. Se você já é assinante, localize o arquivo pelo nome diretamente no canal.*
""")
        
        print(f"✅ Página gerada com sucesso: {titulo_seo}")
        os.system(f"cd {CAMINHO_BASE} && hugo")

# ==========================================
# --- INICIALIZAÇÃO ---
# ==========================================

print("📡 Jotta, o Sentinela do Arquivista está online!")
print("Monitorando grupos VIP para gerar o Top 10 no Google...")

client.start()
client.run_until_disconnected()
