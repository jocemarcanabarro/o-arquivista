import os
import re
import time
from telethon import TelegramClient, events

# --- CREDENCIAIS ---
API_ID = 25177007
API_HASH = 'b2a508d67b45bfd330216410168ff654'
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
        print(f"📦 Detectado: {event.file.name}")
        
        nome_arq = event.file.name
        titulo_seo = formatar_titulo(nome_arq)
        slug = re.sub(r'\W+', '-', titulo_seo.lower()).strip('-')

        # Lógica de Sincronização: Foto deve vir IMEDIATAMENTE antes
        mensagens = await client.get_messages(event.chat_id, limit=2)
        foto_nome = "placeholder.jpg"
        
        if len(mensagens) > 1 and mensagens[1].photo:
            os.makedirs(CAMINHO_FOTOS, exist_ok=True)
            foto_local = await mensagens[1].download_media(file=os.path.join(CAMINHO_FOTOS, f"{slug}.jpg"))
            foto_nome = os.path.basename(foto_local)
            print(f"📸 Foto sincronizada: {foto_nome}")

        os.makedirs(CAMINHO_POSTS, exist_ok=True)
        post_path = os.path.join(CAMINHO_POSTS, f"{slug}.md")

        with open(post_path, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{titulo_seo}"
date: {event.date.isoformat()}
summary: "Arquivo Técnico: {nome_arq}"
cover:
    image: "images/projetos/{foto_nome}"
    alt: "{titulo_seo}"
    hiddenInList: false
    hiddenInSingle: true
---

### 📁 Detalhes do Arquivo
**Nome:** `{nome_arq}`  
**Categoria:** Fabricação Digital (Laser, 3D, Papercraft)

---

### 💎 O VERDADEIRO TESOURO
O acervo **O Arquivista VIP** é o combustível para sua produtividade. Ao assinar, você tem acesso imediato a milhares de projetos premium:

* 🚀 **Corte Laser** (DXF, SVG, LBRN2)
* 🖨️ **Impressão 3D** (STL)
* ✂️ **Papercraft e Sublimação**

**Acelere sua produção e pare de perder tempo desenhando!**

---

### 📥 [CLIQUE AQUI PARA ENTRAR NO GRUPO E BAIXAR]({LINK_FREE})

*As instruções de acesso ao VIP estão fixadas no topo do grupo gratuito.*
""")
        
        # Execução do Hugo e Git
        os.system(f"cd {CAMINHO_BASE} && hugo")
        os.system(f"cd {CAMINHO_BASE} && git add . && git commit -m 'Novo projeto: {titulo_seo}' && git push")
        print(f"🚀 {titulo_seo} publicado em oarquivista.com!")

print("📡 Sentinela Catálogo Online!")
client.start()
client.run_until_disconnected()
