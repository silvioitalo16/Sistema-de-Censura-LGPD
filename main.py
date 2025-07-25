from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import fitz
import shutil
import os
import spacy
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Carrega modelo spaCy em português
nlp = spacy.load("pt_core_news_md")

# Padrões de regex para dados sensíveis
PADROES_REGEX = {
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "TELEFONE": r"\(?\d{2}\)?\s?\d{4,5}-\d{4}",
    "CEP": r"\b\d{5}-\d{3}\b"
}

# Detecta entidades com spaCy
def detectar_entidades_ner(texto):
    doc = nlp(texto)
    dados = []
    for ent in doc.ents:
        if ent.label_ in ["PER", "LOC", "ORG", "DATE"]:
            dados.append(ent.text)
    return dados

# Detecta dados com regex
def detectar_regex(texto):
    encontrados = []
    for label, padrao in PADROES_REGEX.items():
        matches = re.findall(padrao, texto)
        encontrados.extend(matches)
    return encontrados

# Página inicial com formulário
@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Upload via formulário HTML
@app.post("/uploadform")
async def upload_form(file: UploadFile = File(...)):
    response = await upload_file(file)
    censurados = response["dados_censurados"]

    html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Resultado - Anonimizador LGPD</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="header">
        <img src="/static/logo.png" alt="Logo Governo do Estado do Amazonas">
    </div>
    <div class="result">
        <h2>Arquivo processado com sucesso!</h2>
        <p><strong>Dados censurados:</strong></p>
        <ul>
"""
    # Adiciona os itens da lista
    for dado in censurados:
        html += f"<li>{dado}</li>\n"

    # Finaliza o HTML
    html += """
        </ul>
        <a href="/download">📄 Baixar PDF Censurado</a>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html)


# Upload via API (com log)
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Apenas arquivos PDF são permitidos."}

    temp_path = "temp.pdf"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = fitz.open(temp_path)
    texto_total = ""

    for page in doc:
        texto_total += page.get_text()

    dados_ner = detectar_entidades_ner(texto_total)
    dados_regex = detectar_regex(texto_total)
    termos_para_censura = list(set(dados_ner + dados_regex))
    censurados = []

    for page in doc:
        for termo in termos_para_censura:
            areas = page.search_for(termo)
            if areas:
                censurados.append(termo)
            for area in areas:
                page.draw_rect(area, color=(0, 0, 0), fill=(0, 0, 0))

    output_path = "output.pdf"
    doc.save(output_path)
    doc.close()
    os.remove(temp_path)

    return {
        "mensagem": "Arquivo censurado com sucesso!",
        "dados_censurados": list(set(censurados)),
        "download_url": "/download"
    }

# Download do arquivo censurado
@app.get("/download")
async def download_file():
    output_path = "output.pdf"
    if os.path.exists(output_path):
        return FileResponse(output_path, filename="documento_censurado.pdf", media_type="application/pdf")
    return {"error": "Arquivo não encontrado."}

# para executar uvicorn main:app --reload
# fastAPI  http://127.0.0.1:8000/docs

# Framework web e execução
#pip install fastapi uvicorn python-multipart

# Leitura e edição de PDFs
#pip install PyMuPDF

# Processamento de linguagem natural (NLP)
#pip install spacy
#python -m spacy download pt_core_news_md  # modelo em português

# Templates HTML (já incluído no FastAPI, mas pode garantir)
#pip install jinja2

# Para gerar o PDF de documentação (usado neste chat)
#pip install fpdf

# (Opcional) Para depurar problemas com acentuação: unidecode
#pip install unidecode