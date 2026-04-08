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

        # Busca as últimas mensagens para achar a foto
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

        # Gerando o conteúdo com o novo foco em Laser, 3D, Papercraft e Sublimação
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{titulo_seo}"
date: {event.date.isoformat()}
description: "Baixe o vetor {titulo_seo} e conheça o acervo VIP do Arquivista com arquivos para Laser, 3D, Papercraft e Sublimação."
cover:
    image: "images/projetos/{foto_nome}"
    alt: "{titulo_seo}"
    hiddenInList: false
    hiddenInSingle: false
---

![{titulo_seo}](images/projetos/{foto_nome})

O projeto **{titulo_seo}** é apenas uma pequena amostra do que entregamos diariamente para centenas de oficinas e criadores em todo o Brasil.

---

### 🏆 Onde está o verdadeiro tesouro?

Se você busca profissionalismo e quer parar de perder tempo procurando arquivos que não funcionam, o **Arquivista VIP** foi feito para você. 

Ao se tornar um membro VIP, você não acessa apenas este projeto, mas abre as portas para o maior acervo multidisciplinar do Telegram:

* 🚀 **Corte Laser Premium:** Vetores testados em DXF, SVG e AI.
* 🖨️ **Impressão 3D:** Arquivos STL prontos para fatiar.
* ✂️ **Papercraft:** Projetos incríveis para corte em papel.
* 🎨 **Sublimação e muito mais:** Artes em alta resolução.

**Assine O Arquivista VIP e acelere sua produtividade agora mesmo!**

---

### 📥 [CLIQUE AQUI PARA ENTRAR NO GRUPO E BAIXAR]({LINK_FREE})

*Dentro do nosso grupo gratuito, você encontrará as instruções fixadas sobre como acessar o Acervo VIP e garantir seu acesso a todos esses materiais.*
""")
        
        print(f"✅ Página gerada: {titulo_seo}")
        
        # Processa o site com o Hugo
        os.system(f"cd {CAMINHO_BASE} && hugo")
        
        # Envia automaticamente para o GitHub (oarquivista.com)
        print("📤 Enviando para o domínio oarquivista.com...")
        os.system(f"cd {CAMINHO_BASE} && git add . && git commit -m 'Novo projeto VIP: {titulo_seo}' && git push")
        print("🚀 Site atualizado com sucesso!")

# ==========================================
# --- INICIALIZAÇÃO ---
# ==========================================

print("📡 Jotta, o Sentinela do Arquivista está online!")
print("Monitorando VIPs para alimentar o domínio oarquivista.com...")

client.start()
client.run_until_disconnected()
