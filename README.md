🛡️ Anonimizador LGPD – Sistema de Censura Automatizada de Dados Pessoais
Este projeto tem como objetivo oferecer uma solução prática e automatizada para anonimização de documentos digitais, conforme as diretrizes da Lei Geral de Proteção de Dados (LGPD).

A aplicação permite que o usuário envie arquivos PDF contendo possíveis dados pessoais sensíveis (como nomes, CPFs, e-mails, datas, telefones, etc.), e retorna uma versão censurada do documento, com tarjas pretas aplicadas automaticamente sobre as informações identificadas.

💡 Destaques do projeto:
Detecção de entidades sensíveis com NLP (spaCy) e Regex

Manipulação direta de arquivos PDF com PyMuPDF

Backend rápido e leve com FastAPI

Interface web responsiva e institucional (HTML + CSS)

Transparência: lista dos dados censurados exibida ao final da operação

Preparado para uso em ambientes com foco em segurança da informação, compliance e governo digital

🧩 Funcionalidades:
📄 Upload de arquivos PDF

🤖 Identificação automática de:

Nomes de pessoas

Locais, datas e organizações

CPF, e-mail, telefone e CEP

🎯 Aplicação de tarjas pretas sobre os dados encontrados

✅ Geração de documento pronto para distribuição, em conformidade com a LGPD

🏗️ Tecnologias utilizadas:
Python 3.11+

FastAPI

PyMuPDF (fitz)

spaCy (pt_core_news_md)

HTML + CSS puro

Jinja2 Templates
