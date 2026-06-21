# 🏛️ PoliticAI — Análise Inteligente de Governos e Políticos

O **PoliticAI** é um assistente de análise política executado no Google Colab.
Avalia governos com base em dados reais e referências fornecidas pelo usuário,
identificando ações diretas e efeitos propagados — dando crédito a quem merece
e responsabilidade a quem errou. Tudo salvo no seu Google Drive.

---

## 🛡️ Vantagens

| # | Benefício | Detalhe |
|---|-----------|---------|
| 1 | **100% Gratuito** | Roda na infraestrutura do Google + API Groq gratuita |
| 2 | **Sem Instalação** | Pronto para uso direto no navegador |
| 3 | **Drive Integrado** | Relatórios e análises salvos automaticamente |
| 4 | **Baseado em Evidências** | Não inventa nada — só analisa o que você fornece |

---

## 🚀 Como Iniciar

1. No menu superior, clique em **Ambiente de execução → Executar tudo** (ou `Ctrl + F9`).
2. Aguarde ~2 minutos enquanto as dependências são instaladas.
3. Clique no botão que irá aparecer e o PoliticAI abrirá em uma nova aba.
4. Na primeira vez, clique em **"+ provedor IA"** e insira sua chave Groq gratuita
   (obtenha em: https://console.groq.com/keys).

---

## ℹ️ Informações Importantes

- **Navegador:** Use preferencialmente o **Google Chrome**.
- **Internet:** Conexão estável é obrigatória.
- **Google Drive:** Os dados ficam em `Meu Drive/PoliticAI/`.
  - `[Nome do Político]/Estatísticas/` — dados fornecidos pelo usuário sobre o governo
  - `[Nome do Político]/Referências/` — estudos e fontes relacionadas ao governo
  - `[Nome do Político]/Análises/` — relatórios e arquivos gerados pela agente
- **Permissões:** Conceda todas as permissões solicitadas pelo Colab.

---

## 📁 Estrutura do Drive

```
Meu Drive/
└── PoliticAI/
    └── [Nome do Político]/
        ├── Estatísticas/   ← você coloca dados aqui
        ├── Referências/    ← você coloca estudos aqui
        └── Análises/       ← a agente salva os resultados aqui
```

---

## 💬 Exemplos de comandos para o chat

```
"Analisa o governo do Lula com base nos arquivos do Drive."

"Quais foram os efeitos diretos das políticas econômicas do FHC?"

"Gera um relatório de efeitos propagados do governo Dilma."

"Compara os resultados do governo Bolsonaro com os dados de Estatísticas."

"Quais créditos e responsabilidades podem ser atribuídos ao governo Temer?"
```

---

## Célula de execução (cole no Colab):

```python
import os, sys, subprocess, shutil

REPO_URL = "https://github.com/davilucena-dev/PoliticAI.git"
WORK_DIR = "/tmp/politicai"

print("⏳ Carregando o PoliticAI...")

if os.path.exists(WORK_DIR):
    shutil.rmtree(WORK_DIR)

print("📥 Baixando arquivos...")
subprocess.run(["git", "clone", "--depth", "1", REPO_URL, WORK_DIR], capture_output=True)

os.chdir(WORK_DIR)
sys.path.insert(0, WORK_DIR)

from main import run
run()
```

---

## ⚠️ Limitações e Privacidade

O PoliticAI **não substitui** análise acadêmica formal nem consultoria política especializada.
As análises são baseadas exclusivamente nos dados e referências fornecidos pelo usuário
nas pastas do Drive — a agente não inventa, não especula e não opina sem embasamento.

> **Imparcialidade:** O PoliticAI analisa fatos e efeitos sem viés partidário.
> Créditos e responsabilidades são atribuídos com base nos dados fornecidos, não em opinião.

---

## Citação / Créditos

Baseado na arquitetura do **PesquisAI** (Gustavo Bastos Braga, UFV, 2026).
Adaptado para análise de governos e gestão política.

---

*PoliticAI · v1.0 · Análise Política Baseada em Evidências*
