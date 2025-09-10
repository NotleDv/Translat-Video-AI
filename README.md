<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

# 🎬 VIDEO-TRANSLATOR-AI

<em>Construído com as ferramentas e tecnologias:</em>

<img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" alt="JSON">
<img src="https://img.shields.io/badge/Torch-1.0-orange?style=flat&logo=PyTorch&logoColor=white" alt="Torch">
<img src="https://img.shields.io/badge/FFmpeg-007808.svg?style=flat&logo=FFmpeg&logoColor=white" alt="FFmpeg">
<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
<img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black" alt="Hugging Face">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">

</div>

---

## ✨ Visão geral
Este projeto foi desenvolvido para fins estudantis, focando no uso prático de SLMs. Atualmente, traduz vídeos do inglês para português (Brasil) automaticamente. Correções e otimizações serão adicionadas futuramente.

## 🔀 Fluxograma do funcionamento do sistema

<img width="736" alt="Image" src="https://github.com/user-attachments/assets/da2559f0-e0ec-4085-ab01-0a03abd07227" />

---

## 📋 Pré-requisitos

- **Linguagem de Programação:** Python
- **Gerenciador de Pacotes:** [UV](https://docs.astral.sh/uv/getting-started/installation/)
- **Gerenciador de Pacotes Alternativo:** pip
- **Dependências:** FFmpeg ([Download FFmpeg](https://www.ffmpeg.org/download.html))

### Instalação do UV no Linux ou macOS:
  ```sh
   curl -LsSf https://astral.sh/uv/0.8.15/install.sh | sh
   echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
   source ~/.bashrc
  ```
### Instalação do FFmpeg no Linux:
  ```sh
   sudo apt update
   sudo apt install ffmpeg
  ```
### Instalação do rubberband-cli no Linux:
  ```sh
   sudo apt update
   sudo apt install rubberband-cli
  ```
---

## ⚙️ Instalação

1. **Clone o repositório:**
    ```sh
    git clone https://github.com/NotleDv/Translat-Video-AI
    ```
2. **Navegue até o diretório do projeto:**
    ```sh
    cd Translat-Video-AI
    ```
3. **Crie e ative o ambiente virtual principal:**
   ```sh
   uv venv .venv --python=3.10
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
4. **Crie e ative o ambiente virtual secundário:**
   ```sh
   uv venv .venv_ds --python=3.10
   source .venv_ds/bin/activate
   uv pip install -r requirements_ds.txt
   ```


---

## 🔐 Token Hugging Face

Antes de rodar o projeto, acesse este site para criar um token: [pyannote/speaker-diarization-3.1 · Hugging Face](https://huggingface.co/pyannote/speaker-diarization-3.1).

Crie uma conta no Hugging Face, faça o login e gere um token de acesso.

Adicione esse token na chave `token` do arquivo `config.json` na raiz do projeto.

Exemplo: {
"token": "SEU_TOKEN_AQUI"
}


Esta ação deve ser feita antes de rodar o projeto.

---

## 🧪 Vídeo demonstrativo

### 🎞️ **Vídeo original**. [Disponível aqui](https://youtu.be/mVYgtzDLZfY?si=PkiNz47DOFW80PyX)
 
https://github.com/user-attachments/assets/3df87e5e-291b-448f-8587-339b12dbc8ed


### ⭐ **Vídeo dublado**.

https://github.com/user-attachments/assets/cd3ba3d2-0886-4d87-9760-9f002757ed7e





---

## 💻 Como Utilizar

1. **Navegue até o diretório do projeto:**
    ```sh
    cd Translat-Video-AI
    ```
2. **Acesse o .venv:**
    ```sh
    source .venv/bin/activate
    ```
3. **Execute no terminal:**
    ```sh
    python -m pipeline.pipeline
    ```

---

## 🏅 Créditos SLM

- [speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
- [facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M)
- [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- [openai/whisper](https://github.com/openai/whisper)
- [deezer/spleeter](https://github.com/deezer/spleeter)


<div align="left"><a href="#top">⬆ Return</a></div>

---


