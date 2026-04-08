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
    return f"Projeto Corte Laser {titulo} - Arquivo DXF"

@client.on(events.NewMessage(chats=GRUPOS_VIP))
async def handler(event):
    # Só dispara se for um arquivo ZIP/RAR
    if event.file and event.file.ext in ['.zip', '.rar', '.7z']:
        print(f"📦 Novo arquivo detectado: {event.file.name}")
        
        nome_arq = event.file.name
        titulo_seo = formatar_titulo(nome_arq)
        slug = re.sub(r'\W+', '-', titulo_seo.lower()).strip('-')

        # --- LÓGICA DA OPÇÃO A: BUSCAR FOTO IMEDIATAMENTE ANTERIOR ---
        # Buscamos as 2 últimas mensagens (a atual e a anterior)
        mensagens = await client.get_messages(event.chat_id, limit=2)
        foto_nome = "placeholder.jpg" # Caso não ache a foto certa
        
        # A mensagem anterior é a mensagens[1]
        if len(mensagens) > 1 and mensagens[1].photo:
            os.makedirs(CAMINHO_FOTOS, exist_ok=True)
            foto_local = await mensagens[1].download_media(file=os.path.join(CAMINHO_FOTOS, f"{slug}.jpg"))
            foto_nome = os.path.basename(foto_local)
            print(f"📸 Foto sincronizada com sucesso: {foto_nome}")
        else:
            print("⚠️ Aviso: Não encontrei uma foto na mensagem anterior a este arquivo.")

        os.makedirs(CAMINHO_POSTS, exist_ok=True)
        post_path = os.path.join(CAMINHO_POSTS, f"{slug}.md")

        with open(post_path, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{titulo_seo}"
date: {event.date.isoformat()}
description: "Baixe o vetor {titulo_seo} e conheça o acervo VIP do Arquivista com arquivos para Laser, 3D, Papercraft e Sublimação."
cover:
    image: "images/projetos/{foto_nome}"
    alt: "{titulo_seo}"
    hiddenInList: false
    hiddenInSingle: true
---

O projeto **{titulo_seo}** é apenas uma pequena amostra do que entregamos diariamente para centenas de oficinas e criadores em todo o Brasil.

---

### 🏆 Onde está o verdadeiro tesouro?

Se você busca profissionalismo e quer parar de perder tempo procurando arquivos que não funcionam, o **Arquivista VIP** foi feito para você. 

* 🚀 **Corte Laser Premium** | 🖨️ **Impressão 3D** | ✂️ **Papercraft** | 🎨 **Sublimação**

**Assine O Arquivista VIP e acelere sua produtividade!**

---

### 📥 [CLIQUE AQUI PARA ENTRAR NO GRUPO E BAIXAR]({LINK_FREE})

*Dentro do nosso grupo gratuito, você encontrará as instruções fixadas sobre como acessar o Acervo VIP.*
""")
        
        print(f"✅ Página gerada: {titulo_seo}")
        os.system(f"cd {CAMINHO_BASE} && hugo")
        os.system(f"cd {CAMINHO_BASE} && git add . && git commit -m 'Novo projeto VIP: {titulo_seo}' && git push")
        print("🚀 Site atualizado no domínio oarquivista.com!")

# --- INICIALIZAÇÃO ---
print("📡 Sentinela Sincronizado Online!")
client.start()
client.run_until_disconnected()

