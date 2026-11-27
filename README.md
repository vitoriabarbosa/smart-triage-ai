# Smart Triage AI

API de triagem inteligente de mensagens de clientes, utilizando Inteligência Artificial para classificar solicitações e automatizar o fluxo de atendimento.

## 1. Apresentação da Ideia

O projeto surgiu a partir do cenário proposto no desafio técnico da Kodie: uma empresa que recebe diariamente mensagens de clientes e precisa identificar manualmente o assunto de cada uma para encaminhá-las ao setor responsável.

A proposta é utilizar Inteligência Artificial para interpretar essas mensagens e organizar as informações, enquanto uma ferramenta de automação integra as etapas do processo.

## 2. Problema Escolhido

**Classificação de Mensagens**

O recebimento de mensagens com diferentes tipos de dúvidas, reclamações, solicitações e problemas técnicos pode tornar o atendimento desorganizado e consumir tempo da equipe.

O projeto busca facilitar essa organização, identificando automaticamente o tipo de mensagem, sua prioridade e o setor responsável.

## 3. Solução Proposta

O Smart Triage AI utiliza uma API desenvolvida em Python com FastAPI e integrada ao Google Gemini.

A partir de uma mensagem enviada pelo cliente, o modelo de IA realiza a classificação e retorna informações estruturadas em JSON.

A solução identifica:

- **Categoria:** tipo de mensagem recebida.
- **Prioridade:** nível de urgência.
- **Resumo:** síntese do relato do cliente.
- **Setor:** departamento responsável pelo atendimento.
- **Justificativa:** explicação da classificação realizada.

A integração com o n8n permite automatizar a comunicação entre o recebimento da mensagem e a API, além de direcionar a execução conforme o setor identificado.

## 4. Tecnologias Utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem utilizada no desenvolvimento da API |
| FastAPI | Construção da API REST |
| Google Gemini | Interpretação e classificação das mensagens |
| Pydantic | Validação e estruturação dos dados |
| n8n | Orquestração do fluxo de automação |
| Git e GitHub | Versionamento e armazenamento do projeto |

## 5. Funcionamento do Sistema

O funcionamento está dividido em duas partes principais.

### 5.1 API de Triagem

A API disponibiliza o endpoint `POST /triage`, responsável por receber a mensagem do cliente.

O processamento acontece nas seguintes etapas:

1. Recebe a mensagem por meio de uma requisição HTTP.
2. Valida os dados de entrada utilizando Pydantic.
3. Envia o conteúdo para o Google Gemini acompanhado de um prompt estruturado.
4. Recebe a classificação gerada pela IA em formato JSON.
5. Valida e retorna os dados ao solicitante.

### 5.2 Classificação com Inteligência Artificial

O prompt define as categorias, prioridades e setores disponíveis para a classificação.

**Categorias:**
- `duvida`
- `reclamacao`
- `solicitacao`
- `problema_tecnico`

**Prioridades:**
- `baixa`
- `media`
- `alta`

**Setores:**
- `atendimento`
- `relacionamento`
- `administrativo`
- `suporte_tecnico`

A resposta é estruturada para manter um formato consistente e facilitar o processamento pelas próximas etapas.

### 5.3 Fluxo de Automação com n8n

O workflow conecta o recebimento da mensagem à API de triagem e utiliza o resultado da classificação para direcionar o processamento.

O fluxo utiliza os seguintes nodes:

1. **Webhook:** recebe a mensagem enviada pelo cliente por meio de uma requisição POST.
2. **HTTP Request:** encaminha a mensagem para o endpoint `/triage` da API FastAPI.
3. **Switch:** avalia o campo `setor` retornado pela API e direciona a execução para uma das quatro saídas:
   - `atendimento`
   - `relacionamento`
   - `administrativo`
   - `suporte_tecnico`
4. **Respond to Webhook:** retorna ao solicitante o resultado da classificação realizada pela IA.

O workflow exportado está disponível em `n8n/workflow.json`.

### 5.4 Exemplo de Entrada

```json
{
  "mensagem": "Estou tentando acessar minha conta há duas horas, mas aparece um erro e não consigo entrar. Preciso resolver isso com urgência."
}
```

### 5.5 Exemplo de Resposta

```json
{
  "categoria": "problema_tecnico",
  "prioridade": "alta",
  "resumo": "Cliente relata erro ao tentar acessar a conta e solicita resolução urgente.",
  "setor": "suporte_tecnico",
  "justificativa": "O cliente está impedido de utilizar o serviço devido a um erro de acesso e relata urgência, caracterizando um problema técnico de alta prioridade."
}
```

## 6. Como Executar

### 6.1 Pré-requisitos

- Python e pip.
- Node.js e npm.
- n8n instalado.
- Chave de API do Google Gemini.

### 6.2 Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd smart-triage-ai
```

### 6.3 Configurar o Ambiente Python

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 6.4 Configurar as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência.

Configure as variáveis necessárias:

```env
GEMINI_API_KEY=sua_chave_de_api
GEMINI_MODEL=gemini-3.5-flash-lite
```

**Importante:** não compartilhe sua chave de API nem publique o arquivo `.env` no repositório.

### 6.5 Executar a API

Com o ambiente virtual ativado, execute:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

### 6.6 Executar o n8n

Em outro terminal, inicie o n8n:

```bash
n8n start
```

Acesse a interface em:

```text
http://localhost:5678
```

Importe o workflow disponível em `n8n/workflow.json` e execute-o em modo de teste.

Mantenha a API em execução durante os testes do workflow.

## 7. Documentação Visual

As capturas de tela abaixo demonstram a estrutura, as configurações e o funcionamento da automação.

As imagens serão organizadas no diretório `docs/screenshots/`.

| Captura | Descrição |
|---|---|
| `workflow-overview.png` | Visão geral do workflow no n8n, com todos os nodes conectados. |
| `webhook-config.png` | Configuração do Webhook, responsável por receber as mensagens. |
| `http-request-config.png` | Configuração do HTTP Request, responsável por enviar os dados à API FastAPI. |
| `switch-config.png` | Configuração das regras de direcionamento com base no setor identificado. |
| `respond-to-webhook-config.png` | Configuração do retorno da resposta ao solicitante. |
| `workflow-execution.png` | Execução completa do workflow, acompanhada dos logs do Respond to Webhook. |
| `api-terminal.png` | API FastAPI em execução no ambiente virtual Python (.venv). |
| `swagger-docs.png` | Documentação interativa da API no Swagger, demonstrando as rotas disponíveis e os schemas. |

## 8. Estrutura do Projeto

```text
smart-triage-ai/
├── app/
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
├── docs/
│   └── screenshots/
├── n8n/
│   └── workflow.json
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 9. Considerações Finais

O Smart Triage AI demonstra como a Inteligência Artificial pode ser integrada a uma aplicação para interpretar informações e apoiar processos do cotidiano.

A combinação entre API, modelo de IA e automação permite transformar mensagens não estruturadas em informações organizadas, facilitando sua utilização em processos de atendimento.

Projeto desenvolvido como parte do **Desafio Técnico — IA e Automação**, da Kodie.