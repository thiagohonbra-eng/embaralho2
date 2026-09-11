"""
Embaralhador de Músicas
------------------------
App simples com janela (Windows) para reembaralhar a ORDEM de reprodução
de uma pasta de músicas, sem apagar o nome original de cada arquivo.

Como funciona:
- Cada música recebe um prefixo numérico ("01 - ", "02 - ", ...) na frente
  do nome original.
- A cada clique em "Embaralhar", a numeração é sorteada de novo, então a
  ordem alfabética (que é como a maioria dos players/rádios lê a pasta)
  muda também.
- Se um arquivo já tiver um prefixo de uma rodada anterior, ele é removido
  antes de aplicar o novo, então o nome nunca fica "empilhando" números.

Requisitos: Python 3 instalado no Windows (o tkinter já vem junto na
instalação padrão do python.org). Não precisa instalar mais nada.

Como usar:
1. Dê duplo clique neste arquivo (ou rode "python embaralhador_musicas.py")
2. Clique em "Selecionar pasta" e escolha a pasta com as músicas
3. Clique em "Embaralhar" quantas vezes quiser
"""

import os
import re
import random
import tkinter as tk
from tkinter import filedialog, messagebox

# Extensões de áudio reconhecidas
EXTENSOES_AUDIO = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".wma", ".aac"}

# Reconhece um prefixo já aplicado por este app, ex: "07 - "
PADRAO_PREFIXO = re.compile(r"^\d{1,4} - ")


class EmbaralhadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Embaralhador de Músicas")
        self.root.geometry("520x400")
        self.pasta = None

        tk.Label(
            root, text="Embaralhador de Músicas", font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 5))

        self.label_pasta = tk.Label(
            root, text="Nenhuma pasta selecionada", fg="#555", wraplength=480
        )
        self.label_pasta.pack(pady=(0, 10))

        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=5)

        tk.Button(
            frame_botoes, text="Selecionar pasta", width=18,
            command=self.selecionar_pasta
        ).grid(row=0, column=0, padx=5)

        self.btn_embaralhar = tk.Button(
            frame_botoes, text="Embaralhar", width=18,
            command=self.embaralhar, state="disabled", bg="#4CAF50", fg="white"
        )
        self.btn_embaralhar.grid(row=0, column=1, padx=5)

        self.texto_log = tk.Text(root, height=15, width=62, state="disabled")
        self.texto_log.pack(padx=15, pady=15)

    def log(self, msg):
        self.texto_log.config(state="normal")
        self.texto_log.insert("end", msg + "\n")
        self.texto_log.see("end")
        self.texto_log.config(state="disabled")

    def selecionar_pasta(self):
        caminho = filedialog.askdirectory(title="Selecione a pasta com as músicas")
        if not caminho:
            return
        self.pasta = caminho
        arquivos = self._listar_musicas()
        self.label_pasta.config(text=f"Pasta: {caminho}  ({len(arquivos)} músicas encontradas)")
        self.texto_log.config(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.config(state="disabled")
        self.btn_embaralhar.config(state="normal" if arquivos else "disabled")
        if not arquivos:
            messagebox.showwarning("Aviso", "Nenhum arquivo de áudio encontrado nessa pasta.")

    def _listar_musicas(self):
        if not self.pasta:
            return []
        return [
            f for f in os.listdir(self.pasta)
            if os.path.splitext(f)[1].lower() in EXTENSOES_AUDIO
        ]

    def _nome_sem_prefixo(self, nome):
        return PADRAO_PREFIXO.sub("", nome, count=1)

    def embaralhar(self):
        arquivos = self._listar_musicas()
        if not arquivos:
            messagebox.showwarning("Aviso", "Nenhum arquivo de áudio encontrado.")
            return

        random.shuffle(arquivos)
        largura = len(str(len(arquivos)))  # ex: 3 dígitos se tiver 100+ músicas

        # Passo 1: renomeia tudo para nomes temporários, pra evitar qualquer
        # conflito caso dois nomes finais colidam durante o processo.
        temporarios = []
        for nome in arquivos:
            origem = os.path.join(self.pasta, nome)
            temp_nome = "__tmp__" + nome
            destino = os.path.join(self.pasta, temp_nome)
            os.rename(origem, destino)
            temporarios.append((temp_nome, nome))

        # Passo 2: aplica o novo prefixo numérico sorteado
        self.texto_log.config(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.config(state="disabled")
        self.log(f"Nova rodada — {len(arquivos)} músicas embaralhadas:\n")

        for i, (temp_nome, nome_original) in enumerate(temporarios, start=1):
            nome_limpo = self._nome_sem_prefixo(nome_original)
            novo_nome = f"{str(i).zfill(largura)} - {nome_limpo}"
            origem = os.path.join(self.pasta, temp_nome)
            destino = os.path.join(self.pasta, novo_nome)
            os.rename(origem, destino)
            self.log(f"{novo_nome}")

        self.log("\nPronto! Clique em Embaralhar de novo quando quiser outra ordem.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmbaralhadorApp(root)
    root.mainloop()
