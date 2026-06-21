import os
import shutil
import subprocess

SKILLS_DIR = os.path.expanduser("~/.agents/skills")

# Skills específicas da PoliticAI
# Por enquanto usa skills locais (criadas neste arquivo).
# Quando você publicar no GitHub, substitua pelas URLs dos repos.
REMOTE_SKILLS = [
    ("https://github.com/davilucena-dev/Skill-IBGE-PoliticAI.git", "ibge-politicai"),
]

JOKES = [
    "📋 Instalando o manual de análise política...",
    "🔍 Configurando o sistema de atribuição de efeitos...",
    "📊 Preparando os modelos de relatório...",
]

_joke_index = 0

def next_joke():
    global _joke_index
    joke = JOKES[_joke_index % len(JOKES)]
    _joke_index += 1
    return joke


def create_local_skills():
    """Cria as skills locais da PoliticAI diretamente no disco."""

    os.makedirs(SKILLS_DIR, exist_ok=True)

    # ── Skill: leitura-drive ──────────────────────────────────────────────────
    skill_drive_dir = os.path.join(SKILLS_DIR, "leitura-drive")
    os.makedirs(skill_drive_dir, exist_ok=True)

    with open(os.path.join(skill_drive_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
# Skill: Leitura de Arquivos do Drive — PoliticAI

## Propósito
Ler os arquivos das pastas Estatísticas/ e Referências/ de um político
em `/content/drive/My Drive/PoliticAI/[Nome do Político]/`.

## Como Usar
1. Monte o caminho base do político solicitado.
2. Liste os arquivos em Estatísticas/ e Referências/ separadamente.
3. Leia cada arquivo conforme seu tipo (CSV, JSON, TXT, MD).
4. Nunca leia nem escreva fora das pastas autorizadas.

## Leitura por Tipo de Arquivo

### CSV / planilhas
```python
import csv
path = "/content/drive/My Drive/PoliticAI/[Político]/Estatísticas/dados.csv"
with open(path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
```

### JSON
```python
import json
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
```

### TXT / MD / PDF (texto puro)
```python
with open(path, "r", encoding="utf-8") as f:
    texto = f.read()
```

## Listagem de Arquivos
```python
import os
base = "/content/drive/My Drive/PoliticAI/[Político]"
estatisticas = os.listdir(os.path.join(base, "Estatísticas")) if os.path.isdir(os.path.join(base, "Estatísticas")) else []
referencias  = os.listdir(os.path.join(base, "Referências"))  if os.path.isdir(os.path.join(base, "Referências"))  else []
```

## Regras
- Se Estatísticas/ ou Referências/ estiver vazia, informe o usuário.
- Nunca assuma o conteúdo de um arquivo sem lê-lo primeiro.
- Sempre liste os arquivos encontrados antes de iniciar a análise e confirme com o usuário.
""")
    print("✅ Skill leitura-drive criada.")

    # ── Skill: analise-efeitos ────────────────────────────────────────────────
    skill_efeitos_dir = os.path.join(SKILLS_DIR, "analise-efeitos")
    os.makedirs(skill_efeitos_dir, exist_ok=True)

    with open(os.path.join(skill_efeitos_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
# Skill: Análise de Efeitos Diretos e Propagados

## Propósito
Classificar e documentar os efeitos das ações de um governo,
separando o que aconteceu durante o mandato do que se propagou para governos posteriores.

## Definições

### Efeito Direto
- Resultado observado **dentro do período de mandato** do político analisado.
- Exemplo: queda do desemprego de X% para Y% entre ano A e ano B.
- Sempre respaldado por dado em Estatísticas/ ou afirmação em Referências/.

### Efeito Propagado
- Consequência originada em decisão do mandato analisado, mas que só se tornou
  visível em governos posteriores.
- Exemplo: reforma previdenciária aprovada no governo A cujos efeitos fiscais
  apareceram no governo B.
- Sempre identifique: qual decisão, em qual ano, gerou qual consequência posterior.

## Fluxo de Análise

1. **Leia** todos os arquivos de Estatísticas/ e Referências/.
2. **Extraia** indicadores com valores no início e no fim do mandato.
3. **Calcule** a variação: `(valor_fim - valor_inicio) / valor_inicio * 100`.
4. **Classifique** cada variação como melhora, piora ou estável.
5. **Verifique** em Referências/ se há estudos que atribuem efeitos propagados.
6. **Documente** cada efeito com sua fonte.

## Tabela de Efeitos (modelo)
```
| Indicador | Início | Fim | Variação | Tipo | Fonte |
|---|---|---|---|---|---|
| Desemprego | 12% | 8% | -4 p.p. | Direto | desemprego.csv |
| Dívida pública | 60% PIB | 55% PIB | -5 p.p. | Direto | fiscal.csv |
| Endividamento familiar | — | crise 2015 | — | Propagado | estudo_ipea.pdf |
```

## Regras
- Nunca classifique um efeito sem fonte.
- Se a causalidade for incerta, diga "possível efeito propagado — dados insuficientes para confirmar".
- Não atribua efeitos de um governo a outro sem embasamento documental.
""")
    print("✅ Skill analise-efeitos criada.")

    # ── Skill: atribuicao-creditos ────────────────────────────────────────────
    skill_cred_dir = os.path.join(SKILLS_DIR, "atribuicao-creditos")
    os.makedirs(skill_cred_dir, exist_ok=True)

    with open(os.path.join(skill_cred_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
# Skill: Atribuição de Créditos e Responsabilidades

## Propósito
Atribuir formalmente créditos (melhorias) e responsabilidades (problemas)
ao governo analisado, com base exclusivamente nos arquivos fornecidos.

## Definições

### Crédito
- Atribuído quando uma **melhoria mensurável** pode ser ligada a uma **ação ou política**
  do governo analisado, sustentada por dado ou estudo nos arquivos.

### Responsabilidade
- Atribuída quando um **problema mensurável** pode ser ligado a uma **omissão, decisão
  ou política** do governo analisado, sustentada por dado ou estudo nos arquivos.

## Critérios de Atribuição

| Situação | Atribuição |
|---|---|
| Melhoria com dado + política identificada | ✅ Crédito confirmado |
| Melhoria com dado, sem política identificada | ⚠️ Crédito possível — correlação, não causalidade |
| Piora com dado + decisão identificada | ❌ Responsabilidade confirmada |
| Piora com dado, sem decisão identificada | ⚠️ Responsabilidade possível — dados insuficientes |
| Efeito sem dado nos arquivos | 🚫 Não atribuir — sem evidência |

## Formato de Saída

### Créditos
```
✅ [CRÉDITO CONFIRMADO] Redução da pobreza extrema em X%
   - Dado: pobreza.csv (linha 42) — variação de A% para B%
   - Política associada: Programa Y (referência: estudo_z.pdf, p.12)
```

### Responsabilidades
```
❌ [RESPONSABILIDADE CONFIRMADA] Aumento da dívida pública em X% do PIB
   - Dado: fiscal.csv — dívida passou de A% para B% do PIB
   - Decisão associada: expansão de gastos sem contrapartida (referência: relatorio_w.pdf)
```

### Incertezas
```
⚠️ [ATRIBUIÇÃO INCERTA] Correlação com queda na educação
   - Dado presente, mas causalidade não documentada nos arquivos fornecidos.
   - Recomendação: fornecer estudos adicionais em Referências/.
```

## Regras
- Nunca atribua sem fonte explícita.
- Sempre indique o arquivo e, se possível, a página ou linha do dado.
- Distingua correlação de causalidade.
- Não use linguagem partidária ou emocional.
""")
    print("✅ Skill atribuicao-creditos criada.")

    # ── Skill: gestao-analises ────────────────────────────────────────────────
    skill_analises_dir = os.path.join(SKILLS_DIR, "gestao-analises")
    os.makedirs(skill_analises_dir, exist_ok=True)

    with open(os.path.join(skill_analises_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
# Skill: Gestão de Arquivos de Análise

## Propósito
Criar, salvar e organizar os arquivos gerados pela PoliticAI
na pasta Análises/ do político correspondente.

## Caminho Base
```
/content/drive/My Drive/PoliticAI/[Nome do Político]/Análises/
```

## Criar pasta Análises/ se não existir
```python
import os
analises_path = f"/content/drive/My Drive/PoliticAI/{politico}/Análises"
os.makedirs(analises_path, exist_ok=True)
```

## Tipos de Arquivo e Nomenclatura

| Tipo | Nome do Arquivo |
|---|---|
| Relatório completo | `relatorio_[NomePolitico]_[DDMMAAAA].md` |
| Resumo executivo | `resumo_[NomePolitico]_[DDMMAAAA].md` |
| Tabela de indicadores | `indicadores_[NomePolitico]_[DDMMAAAA].csv` |
| Comparativo entre governos | `comparativo_[PoliticoA]_vs_[PoliticoB]_[DDMMAAAA].md` |
| Log de análises | `log_analises.log` |

## Salvar Relatório Markdown
```python
from datetime import datetime
data = datetime.now().strftime("%d%m%Y")
nome_arquivo = f"relatorio_{politico.replace(' ', '_')}_{data}.md"
caminho = os.path.join(analises_path, nome_arquivo)
with open(caminho, "w", encoding="utf-8") as f:
    f.write(conteudo_relatorio)
```

## Salvar Tabela de Indicadores CSV
```python
import csv
nome_csv = f"indicadores_{politico.replace(' ', '_')}_{data}.csv"
caminho_csv = os.path.join(analises_path, nome_csv)
with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["indicador", "valor_inicio", "valor_fim", "variacao", "fonte"])
    for row in indicadores:
        w.writerow(row)
```

## Registrar no Log
```python
from datetime import datetime
log_path = os.path.join(analises_path, "log_analises.log")
def registrar_log(politico, tipo_analise, arquivos_lidos):
    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] ANÁLISE | {politico} — {tipo_analise} | Arquivos lidos: {arquivos_lidos}\\n")
```

## Regras
- Nunca sobrescreva um arquivo existente sem confirmação do usuário.
- Sempre registre no log após gerar qualquer arquivo.
- Ao final de toda escrita, exiba a mensagem:
  `[📄 Arquivo Gerado] NOME — salvo em PoliticAI/[Político]/Análises/`
""")
    print("✅ Skill gestao-analises criada.")

    # ── Skill: comparativo-governos ───────────────────────────────────────────
    skill_comp_dir = os.path.join(SKILLS_DIR, "comparativo-governos")
    os.makedirs(skill_comp_dir, exist_ok=True)

    with open(os.path.join(skill_comp_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
# Skill: Comparativo entre Governos

## Propósito
Comparar dois ou mais governos nos mesmos indicadores,
com base nos arquivos disponíveis para cada um no Drive.

## Pré-requisitos
- Arquivos em Estatísticas/ de ambos os políticos com indicadores em comum.
- Se um dos políticos não tiver arquivos, informe o usuário antes de prosseguir.

## Fluxo de Comparação

1. Liste os indicadores disponíveis para cada político.
2. Identifique os indicadores em comum.
3. Para cada indicador em comum, extraia: valor_inicio, valor_fim, variacao.
4. Monte a tabela comparativa.
5. Identifique qual governo teve melhor desempenho em cada indicador — **sem julgamento global**.
6. Salve o comparativo em Análises/ de ambos os políticos.

## Tabela Comparativa (modelo)
```
| Indicador | [Político A] início | [Político A] fim | [Político B] início | [Político B] fim | Melhor resultado |
|---|---|---|---|---|---|
| Desemprego | 12% | 8% (-4pp) | 8% | 11% (+3pp) | Político A |
| Inflação | 9% | 4% (-5pp) | 4% | 6% (+2pp) | Político A |
| PIB crescimento | 1% | 4% (+3pp) | 5% | 2% (-3pp) | Político B |
```

## Regras
- "Melhor resultado" é definido pelo dado — nunca por opinião.
- Se os períodos forem diferentes, indique isso claramente na tabela.
- Não faça ranking geral de "melhor governo" — apenas compare indicador a indicador.
- Se faltar dado para um dos lados da comparação, deixe a célula como "sem dado".
""")
    print("✅ Skill comparativo-governos criada.")


def install_skills():
    os.chdir("/tmp")
    print(f"\n{next_joke()}")
    print("🔧 Instalando skills da PoliticAI...")

    create_local_skills()

    # Se houver skills remotas no GitHub, clonar aqui
    for repo_url, name in REMOTE_SKILLS:
        tmp = f"/tmp/skill_{name}"
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, tmp],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            dest = os.path.join(SKILLS_DIR, name)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(tmp, dest, dirs_exist_ok=True)
            print(f"✅ {name} instalada do GitHub.")
        else:
            print(f"❌ Falha ao clonar {repo_url}")

    print(f"\n{next_joke()}")
    print("\n🎉 Todas as skills da PoliticAI instaladas!")


if __name__ == "__main__":
    install_skills()
