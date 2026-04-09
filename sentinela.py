import os
import re
import time
import random
from telethon import TelegramClient, events

# --- CREDENCIAIS ---
API_ID = 25177007
API_HASH = 'b2a508d67b45bfd330216410168ff654'
# IDs dos Grupos (Exemplo: Laser e 3D)
GRUPOS_VIP = [-1002477218350, -1002488469430]
LINK_FREE = "https://t.me/O_Arquivista"

# --- CAMINHOS ---
CAMINHO_BASE = '/data/data/com.termux/files/home/o-arquivista/'
CAMINHO_POSTS = os.path.join(CAMINHO_BASE, 'content/posts/')
CAMINHO_FOTOS = os.path.join(CAMINHO_BASE, 'static/images/projetos/')

client = TelegramClient('sessao_jotta', API_ID, API_HASH)

def formatar_titulo(nome_arquivo):
    titulo = re.sub(r'\.(zip|rar|7z|dxf|lbrn2|svg|ai|cdr)', '', nome_arquivo, flags=re.IGNORECASE)
    titulo = titulo.replace('_', ' ').replace('-', ' ').title()
    return f"{titulo}"

@client.on(events.NewMessage(chats=GRUPOS_VIP))
async def handler(event):
    if event.file and event.file.ext in ['.zip', '.rar', '.7z']:
        print(f"📦 Novo arquivo: {event.file.name}")
        
        nome_arq = event.file.name
        titulo_seo = formatar_titulo(nome_arq)
        slug = re.sub(r'\W+', '-', titulo_seo.lower()).strip('-')

        # Lógica de Categorias Dinâmicas
        if event.chat_id == -1002488469430:
            categoria = "Impressão 3D"
        else:
            categoria = "Corte Laser"

        # Buscar foto anterior
        mensagens = await client.get_messages(event.chat_id, limit=2)
        foto_nome = "placeholder.jpg"
        if len(mensagens) > 1 and mensagens[1].photo:
            os.makedirs(CAMINHO_FOTOS, exist_ok=True)
            foto_local = await mensagens[1].download_media(file=os.path.join(CAMINHO_FOTOS, f"{slug}.jpg"))
            foto_nome = os.path.basename(foto_local)

        os.makedirs(CAMINHO_POSTS, exist_ok=True)
        post_path = os.path.join(CAMINHO_POSTS, f"{slug}.md")

        with open(post_path, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{titulo_seo}"
date: {event.date.isoformat()}
categories: ["{categoria}"]
summary: "Arquivo Técnico: {nome_arq}"
cover:
    image: "images/projetos/{foto_nome}"
    alt: "{titulo_seo}"
    hiddenInList: false
    hiddenInSingle: false
---

### 📁 Detalhes do Projeto
**Arquivo:** `{nome_arq}`  
**Categoria:** {categoria}

---

### 💎 O VERDADEIRO TESOURO
O acervo **O Arquivista VIP** é o combustível para sua produtividade. Acesso imediato:
* 🚀 **Laser** | 🖨️ **3D** | ✂️ **Papercraft** | 🎨 **Sublimação**

---

### 📥 [BAIXAR NO GRUPO GRATUITO]({LINK_FREE})
""")
        
        # Deploy
        os.system(f"cd {CAMINHO_BASE} && hugo")
        os.system(f"cd {CAMINHO_BASE} && git add . && git commit -m 'Novo {categoria}: {titulo_seo}' && git push")
        print(f"✅ Publicado: {titulo_seo} em {categoria}")

print("📡 Sentinela O Arquivista Online!")
client.start()
client.run_until_disconnected()
