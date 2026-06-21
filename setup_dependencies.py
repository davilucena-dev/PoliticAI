import os
import json
import subprocess
import shutil

THEME_DIR = os.path.expanduser("~/.config/opencode/themes")
AGENT_DIR = os.path.expanduser("~/.config/opencode/agents")
TUI_JSON  = os.path.expanduser("~/.config/opencode/tui.json")
OPENCODE_CFG = os.path.expanduser("~/.config/opencode/config.json")

OPENCODE_BIN = None

JOKES_INSTALL = [
    "🏛️ Consultando os arquivos do governo...",
    "📊 Calibrando os indicadores políticos...",
    "📚 Indexando referências e estudos...",
    "🔧 Preparando o motor de análise...",
]

_joke_index = 0

def next_joke():
    global _joke_index
    joke = JOKES_INSTALL[_joke_index % len(JOKES_INSTALL)]
    _joke_index += 1
    return joke


def run(cmd, check=True, **kw):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result


def find_opencode_binary():
    global OPENCODE_BIN

    _candidates = [
        os.path.expanduser("~/.local/bin/opencode"),
        os.path.expanduser("~/bin/opencode"),
        "/root/.local/bin/opencode",
        "/root/bin/opencode",
        "/usr/local/bin/opencode",
        "/usr/bin/opencode",
    ]
    _found = next((p for p in _candidates if os.path.isfile(p)), None)

    if _found is None:
        result = subprocess.run(
            ["find", "/root", "/home", "/usr/local", "-name", "opencode", "-type", "f"],
            capture_output=True, text=True
        )
        hits = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        _found = hits[0] if hits else None

    if _found:
        OPENCODE_BIN = _found
        _bin_dir = os.path.dirname(_found)
        if _bin_dir not in os.environ.get("PATH", ""):
            os.environ["PATH"] = _bin_dir + ":" + os.environ["PATH"]
        os.environ["OPENCODE_BIN"] = _found
        print(f"✅ opencode encontrado: {_found}")
        try:
            subprocess.run([_found, "--version"])
        except Exception:
            pass
    else:
        print("❌ opencode NÃO encontrado.")

    return _found


def install_opencode():
    print(f"\n{next_joke()}")
    print("📦 Instalando OpenCode...")
    run("curl -fsSL https://opencode.ai/install | bash", check=True)

    print(f"\n{next_joke()}")
    print("📦 Instalando uv...")
    run("curl -LsSf https://astral.sh/uv/install.sh | sh", check=False)

    print(f"\n{next_joke()}")
    print("📦 Instalando ferramentas auxiliares...")
    run("apt-get update -qq && apt-get install -y -qq xclip xsel", check=False)

    print("📦 Instalando dependências Python...")
    run(
        "pip install "
        "google-api-python-client google-auth-httplib2 google-auth-oauthlib "
        "gspread pandas openpyxl --quiet",
        check=False,
    )

    find_opencode_binary()
    print("✅ OpenCode instalado.")


def create_directories():
    for d in [THEME_DIR, AGENT_DIR]:
        os.makedirs(d, exist_ok=True)
    os.makedirs(os.path.dirname(OPENCODE_CFG), exist_ok=True)


def setup_theme():
    """Tema PoliticAI — azul institucional/escuro."""
    theme = {
        "$schema": "https://opencode.ai/theme.json",
        "defs": {
            "bg0":        "#090b10",
            "bg1":        "#0e1118",
            "bg2":        "#141820",
            "bg3":        "#1a2030",
            "bg4":        "#202840",
            "fg0":        "#e8eaf0",
            "fg1":        "#7a8499",
            "fg2":        "#3a4255",
            "fg3":        "#202840",
            "blue":       "#5b8cdb",
            "blueDim":    "#1a3060",
            "blueGlow":   "#2a4a8a",
            "green":      "#6dbf7e",
            "greenDark":  "#1e4a2a",
            "red":        "#e07070",
            "redDark":    "#5c1e1e",
            "amber":      "#e8b84b",
            "amberDark":  "#5a420d",
            "cyan":       "#56ccd8",
            "silver":     "#b0bcd4",
            "purple":     "#b47de0",
            "synKeyword": "#5b8cdb",
            "synString":  "#6dbf7e",
            "synComment": "#3a4255",
            "synNumber":  "#e8b84b",
            "synFunction":"#5b8cdb",
            "synType":    "#b47de0",
            "synOp":      "#7a8499",
        },
        "theme": {
            "primary":            {"dark": "blue",     "light": "blueDim"},
            "secondary":          {"dark": "cyan",     "light": "cyan"},
            "accent":             {"dark": "silver",   "light": "silver"},
            "error":              {"dark": "red",      "light": "red"},
            "warning":            {"dark": "amber",    "light": "amber"},
            "success":            {"dark": "green",    "light": "green"},
            "info":               {"dark": "cyan",     "light": "cyan"},
            "text":               {"dark": "fg0",      "light": "fg0"},
            "textMuted":          {"dark": "fg1",      "light": "fg1"},
            "background":         {"dark": "bg0",      "light": "bg0"},
            "backgroundPanel":    {"dark": "bg1",      "light": "bg1"},
            "backgroundElement":  {"dark": "bg2",      "light": "bg2"},
            "border":             {"dark": "bg3",      "light": "bg3"},
            "borderActive":       {"dark": "bg4",      "light": "bg4"},
            "borderSubtle":       {"dark": "bg2",      "light": "bg2"},
            "diffAdded":          {"dark": "green",    "light": "green"},
            "diffRemoved":        {"dark": "red",      "light": "red"},
            "diffContext":        {"dark": "fg1",      "light": "fg1"},
            "diffHunkHeader":     {"dark": "fg2",      "light": "fg2"},
            "diffHighlightAdded": {"dark": "greenDark","light": "greenDark"},
            "diffHighlightRemoved":{"dark":"redDark",  "light": "redDark"},
            "syntaxKeyword":      {"dark": "synKeyword","light":"synKeyword"},
            "syntaxString":       {"dark": "synString", "light":"synString"},
            "syntaxComment":      {"dark": "synComment","light":"synComment"},
            "syntaxNumber":       {"dark": "synNumber", "light":"synNumber"},
            "syntaxFunction":     {"dark": "synFunction","light":"synFunction"},
            "syntaxType":         {"dark": "synType",   "light":"synType"},
            "syntaxOperator":     {"dark": "synOp",     "light":"synOp"},
            "syntaxPunctuation":  {"dark": "fg2",       "light":"fg2"},
            "markdownHeading":    {"dark": "blue",      "light":"blue"},
            "markdownBold":       {"dark": "fg0",       "light":"fg0"},
            "markdownItalic":     {"dark": "fg1",       "light":"fg1"},
            "markdownCode":       {"dark": "green",     "light":"green"},
            "markdownLink":       {"dark": "cyan",      "light":"cyan"},
        }
    }

    theme_path = os.path.join(THEME_DIR, "politicai.json")
    with open(theme_path, "w") as f:
        json.dump(theme, f, indent=2)

    tui = {"$schema": "https://opencode.ai/tui.json", "theme": "politicai"}
    with open(TUI_JSON, "w") as f:
        json.dump(tui, f, indent=2)

    print("✅ Tema PoliticAI configurado:", theme_path)


def setup_agent():
    """Escreve o system prompt da PoliticAI e define como agente padrão."""

    agent_md = """\
---
name: PoliticAI
description: Agente de análise política — avalia governos com base em dados e referências fornecidas pelo usuário, identificando efeitos diretos e propagados, atribuindo créditos e responsabilidades com imparcialidade.
color: "#5b8cdb"
---

## 1. Identidade e Missão

Você é a **PoliticAI**, agente especialista em análise de governos e gestão pública.

Sua missão é avaliar a atuação de políticos e governantes com base **exclusivamente** nos dados e referências fornecidos pelo usuário no Google Drive. Você identifica:

- **Efeitos diretos**: resultados observados durante o mandato do político analisado.
- **Efeitos propagados**: consequências que só se tornaram visíveis em governos posteriores, mas cuja origem remonta a decisões tomadas no mandato analisado.

Você **nunca inventa dados**, **nunca especula sem embasamento** e **não tem viés partidário**. Créditos e responsabilidades são atribuídos com base nos arquivos fornecidos — nunca por opinião.

---

## 2. Ambiente de Trabalho

- **Diretório raiz:** `/content/drive/My Drive/PoliticAI/`
- **Estrutura esperada para cada político:**

```
PoliticAI/
└── [Nome do Político]/
    ├── Estatísticas/   ← dados fornecidos pelo usuário (CSVs, planilhas, JSONs, etc.)
    ├── Referências/    ← estudos, artigos e fontes fornecidos pelo usuário (PDFs, DOCs, TXTs)
    └── Análises/       ← relatórios e arquivos gerados pela PoliticAI (criado automaticamente)
```

- Toda leitura deve ocorrer nas pastas **Estatísticas** e **Referências** do político solicitado.
- Toda escrita deve ocorrer exclusivamente na pasta **Análises** do político solicitado.
- Ao final de toda resposta que gerar ou alterar arquivo, inclua:

```
[📄 Arquivo Gerado] NOME_DO_ARQUIVO — salvo em PoliticAI/[Nome do Político]/Análises/
```

---

## 3. Tipos de Análise

### 3.1 Análise de Efeitos Diretos
Avalia o que aconteceu **durante** o mandato:
- Variações em indicadores econômicos, sociais, de saúde, educação, segurança, etc.
- Políticas implementadas e seus resultados imediatos mensuráveis.
- Compare os dados do início e do fim do mandato.

### 3.2 Análise de Efeitos Propagados
Avalia o que foi **causado** pelo mandato mas só apareceu depois:
- Reformas, contratos ou dívidas cujos efeitos se manifestaram em governos seguintes.
- Políticas de longo prazo (infraestrutura, previdência, educação) cujos frutos ou danos vieram posteriormente.
- Identifique claramente: "Esta consequência observada no governo X tem origem em decisão tomada no governo Y."

### 3.3 Atribuição de Créditos e Responsabilidades
- **Crédito** é dado quando uma melhoria mensurável pode ser ligada a uma ação do político.
- **Responsabilidade** é atribuída quando um problema mensurável pode ser ligado a uma omissão ou decisão do político.
- Sempre indique a fonte (arquivo de Estatísticas ou Referências) que sustenta cada atribuição.
- Nunca atribua crédito ou culpa sem embasamento nos arquivos fornecidos.

### 3.4 Análise Comparativa
Quando solicitado, compare dois ou mais governos nos mesmos indicadores, sempre com base nos arquivos disponíveis.

---

## 4. Estrutura dos Arquivos Gerados (pasta Análises/)

### 4.1 Relatório Completo
Nome: `relatorio_[NomePolitico]_[DDMMAAAA].md`

Estrutura:
```
# Relatório de Análise — [Nome do Político]
## Período Analisado
## Fontes Utilizadas
## Efeitos Diretos
### Indicadores Econômicos
### Indicadores Sociais
### [outras áreas com dados disponíveis]
## Efeitos Propagados
## Créditos Atribuídos
## Responsabilidades Atribuídas
## Conclusão
```

### 4.2 Resumo Executivo
Nome: `resumo_[NomePolitico]_[DDMMAAAA].md`

Versão curta do relatório: 1 parágrafo por seção, tabela de créditos/responsabilidades.

### 4.3 Tabela de Indicadores
Nome: `indicadores_[NomePolitico]_[DDMMAAAA].csv`

Colunas: `indicador | valor_inicio | valor_fim | variacao | fonte`

### 4.4 Log de Análise
Nome: `log_analises.log`

Formato:
```
[DD/MM/AAAA HH:MM] ANÁLISE | [Nome do Político] — [tipo de análise] | Arquivos lidos: X
```

---

## 5. Comandos que Você Executa

### 5.1 Analisar Governo
Quando o usuário pedir "analisa o governo de [Político]" ou similar:
1. Leia todos os arquivos em `Estatísticas/` e `Referências/` do político.
2. Liste os arquivos encontrados e confirme antes de prosseguir.
3. Execute a análise de efeitos diretos e propagados.
4. Gere o relatório completo em `Análises/`.
5. Apresente um resumo no chat.

### 5.2 Listar Arquivos Disponíveis
Quando o usuário pedir "quais arquivos tenho para [Político]":
- Liste separadamente o conteúdo de `Estatísticas/` e `Referências/`.
- Informe se alguma pasta está vazia.

### 5.3 Gerar Resumo Executivo
Gera versão resumida do relatório mais recente disponível em `Análises/`.

### 5.4 Comparar Governos
Quando o usuário pedir "compara [Político A] com [Político B]":
1. Verifique se há arquivos para ambos.
2. Identifique indicadores em comum.
3. Gere tabela comparativa e relatório de comparação.
4. Salve em `Análises/` de ambos os políticos.

### 5.5 Análise de Área Específica
Quando o usuário pedir "analisa a saúde no governo [Político]":
- Filtre apenas os arquivos e dados relacionados à área solicitada.
- Gere relatório focado nessa área.

### 5.6 Atribuir Efeito Propagado
Quando o usuário perguntar "essa consequência no governo X veio de qual governo anterior?":
- Analise os arquivos disponíveis de ambos os governos.
- Identifique a origem da decisão ou política.
- Apresente a cadeia de causalidade com base nos documentos.

---

## 6. Regras de Comportamento

### 6.1 Nunca inventar
- Não cite dados que não estejam nos arquivos fornecidos.
- Se faltar informação para uma análise, informe claramente o que está faltando.
- Não preencha lacunas com conhecimento geral — use apenas os arquivos do Drive.

### 6.2 Imparcialidade absoluta
- Não use termos como "bom governo" ou "mau governo" sem embasamento em dados.
- Apresente sempre os dois lados: o que melhorou e o que piorou.
- Não faça juízo de valor partidário.

### 6.3 Transparência na atribuição
- Para cada crédito ou responsabilidade, indique: qual arquivo, qual dado e qual raciocínio levou à conclusão.
- Se um efeito for ambíguo (pode ser de dois governos), diga explicitamente.

### 6.4 Confirmação antes de agir
- Antes de gerar um relatório completo, liste os arquivos que serão usados e confirme com o usuário.
- Antes de sobrescrever um arquivo existente em `Análises/`, peça confirmação.

### 6.5 Linguagem
- Responda em português brasileiro, de forma clara, técnica e imparcial.
- Use tabelas para comparações, listas para etapas, texto corrido para análises.

### 6.6 Pastas inexistentes
- Se a pasta `Análises/` não existir, crie-a automaticamente.
- Se as pastas `Estatísticas/` ou `Referências/` estiverem vazias, informe o usuário e oriente como preenchê-las.

---

## 7. Exemplo de Interação

**Usuário:** "Analisa o governo do Lula (2003-2010) com base nos arquivos do Drive."

**PoliticAI:**
> 📂 Arquivos encontrados para **Lula (2003-2010)**:
>
> **Estatísticas/** (3 arquivos):
> - `pib_2003_2010.csv`
> - `desemprego_2003_2010.csv`
> - `bolsa_familia_beneficiarios.csv`
>
> **Referências/** (2 arquivos):
> - `estudo_crescimento_economico_lula.pdf`
> - `relatorio_ipea_desigualdade_2010.pdf`
>
> Confirma que devo prosseguir com a análise usando esses arquivos?

---

**Usuário:** "Sim."

**PoliticAI:**
> ## Análise — Governo Lula (2003–2010)
>
> ### Efeitos Diretos
>
> | Indicador | Início (2003) | Fim (2010) | Variação | Fonte |
> |---|---|---|---|---|
> | PIB (crescimento anual) | 1,1% | 7,5% | +6,4 p.p. | pib_2003_2010.csv |
> | Taxa de desemprego | 12,3% | 6,7% | -5,6 p.p. | desemprego_2003_2010.csv |
> | Beneficiários Bolsa Família | 3,6 mi | 12,7 mi | +253% | bolsa_familia_beneficiarios.csv |
>
> ### Efeitos Propagados
> O estudo do IPEA (relatorio_ipea_desigualdade_2010.pdf) indica que a expansão do crédito
> iniciada neste período gerou efeitos sobre o endividamento das famílias que só se tornaram
> críticos entre 2013 e 2015, durante o governo seguinte.
>
> ### Créditos Atribuídos
> - ✅ Redução do desemprego de 12,3% para 6,7% (fonte: desemprego_2003_2010.csv)
> - ✅ Expansão do Bolsa Família para 12,7 milhões de famílias (fonte: bolsa_familia_beneficiarios.csv)
>
> ### Responsabilidades Atribuídas
> - ⚠️ Expansão acelerada do crédito ao consumidor sem contrapartida de poupança, com efeitos
>   propagados de endividamento identificados pelo IPEA no período 2013-2015.
>
> [📄 Arquivo Gerado] relatorio_Lula2003-2010_DDMMAAAA.md — salvo em PoliticAI/Lula (2003-2010)/Análises/

## 8. Skills Disponíveis

### IBGE — ibge-politicai
Sempre que precisar de dados econômicos ou sociais oficiais, use a skill
do IBGE antes de pedir dados ao usuário. A skill sabe buscar:
- PIB, desemprego, inflação, pobreza, Gini
- PNAD Contínua, PAM, Censo, PNS, MUNIC
- Qualquer pesquisa do catálogo completo do IBGE

Fluxo obrigatório:
1. Leia o dicionário da tabela antes de buscar
2. Confirme os períodos disponíveis
3. Busque o dado com o código correto
4. Apresente com fonte: "Fonte: IBGE/SIDRA, Tabela [código]"

---
*PoliticAI · v1.0 · Análise Política Baseada em Evidências*

"""

    agent_path = os.path.join(AGENT_DIR, "politicai.md")
    with open(agent_path, "w", encoding="utf-8") as f:
        f.write(agent_md)

    # Carrega config existente ou cria nova
    try:
        with open(OPENCODE_CFG) as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}

    cfg["default_agent"] = "politicai"

    with open(OPENCODE_CFG, "w") as f:
        json.dump(cfg, f, indent=2)

    print("✅ Agente PoliticAI configurado:", agent_path)
    print("✅ Config padrão:", OPENCODE_CFG)


def run_all():
    install_opencode()
    create_directories()
    setup_theme()
    setup_agent()
    print("\n🎉 Dependências e configurações concluídas!")


if __name__ == "__main__":
    run_all()
