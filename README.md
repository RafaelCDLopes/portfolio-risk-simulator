## 📈 Portfolio Risk Simulator

Aplicação web em **Streamlit** para simular o comportamento de um portfólio de ativos, calcular métricas de risco clássicas e visualizar cenários de Monte Carlo de forma interativa.

### ✨ Principais funcionalidades

- **Simulação de carteira** com pesos customizáveis por ativo.
- **Download automático de preços históricos** via `yfinance`.
- Cálculo de **retorno esperado**, **volatilidade**, **Sharpe**, **VaR**, **CVaR** e **máximo drawdown**.
- **Simulações de Monte Carlo** vetorizadas.
- **Visualizações interativas**:
  - Retorno acumulado do portfólio.
  - Distribuição de retornos e linha de VaR.
  - Matriz de correlação entre ativos.
  - Trajetórias simuladas do portfólio.
- Interface organizada em **abas (Resumo / Risco & correlação / Cenários Monte Carlo)**.

---

## 🚀 Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/portfolio-risk-simulator.git
cd portfolio-risk-simulator
```

### 2. Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux / macOS
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o app Streamlit

```bash
streamlit run app.py
```

Abra o link que aparecer no terminal (geralmente `http://localhost:8501`).

---

## 🧠 Como o simulador funciona

### Arquitetura

- `app.py`  
  Configura o Streamlit (layout, ícone, sidebar) e faz o roteamento para o **PortfolioController**.

- `src/controllers/portfolio_controller.py`  
  Orquestra o fluxo:
  - Lê os inputs da `PortfolioView`.
  - Carrega dados de preços com o `DataLoader`.
  - Cria o `PortfolioModel` e calcula métricas.
  - Executa a simulação de Monte Carlo com `MonteCarloService`.
  - Envia tudo de volta para a view exibir em abas.

- `src/views/portfolio_view.py`  
  Camada de apresentação (Streamlit):
  - Inputs de tickers, datas, simulações e pesos.
  - Componentes visuais (tabelas, gráficos, métricas, abas).

- `src/services/data_loader.py`  
  Serviço de dados:
  - Faz download de séries de preços via `yfinance`.
  - Aplica validações de datas e limpeza dos dados.

- `src/services/simulation_service.py`  
  Serviço de simulação:
  - Implementa a simulação de Monte Carlo de forma **vetorizada com NumPy**, evitando loops pesados.

- `src/models/portfolio_models.py`  
  Modelo quantitativo do portfólio:
  - Calcula retornos, retorno esperado, volatilidade, Sharpe, VaR, CVaR e drawdown.
  - Fornece utilitários estáticos para retornos e matriz de correlação.

---

## 🧪 Exemplo de uso

1. Rode o app com `streamlit run app.py`.
2. Na tela principal:
   - Informe os **tickers** no formato do Yahoo Finance (ex.: `PETR4.SA, VALE3.SA, ITUB4.SA`).
   - Ajuste a **janela de datas** (data inicial e final).
   - Defina o número de **simulações de Monte Carlo** (ex.: 1.000, 5.000, 10.000).
   - Ajuste os **pesos** dos ativos (os valores são normalizados na soma).
3. Clique em **“🚀 Rodar simulação”** e navegue pelas abas de resultados.

---

## ⚙️ Stack e dependências principais

- Python
- Streamlit
- NumPy
- Pandas
- Matplotlib / Seaborn
- yfinance

Todas as versões utilizadas estão especificadas em `requirements.txt`.

---

## 🌍 Short description (English)

**Portfolio Risk Simulator** is a Streamlit app to simulate portfolio behavior, compute classical risk metrics (expected return, volatility, Sharpe, VaR, CVaR, max drawdown) and run Monte Carlo scenarios using historical prices from Yahoo Finance.  
The interface is organized in tabs and the Monte Carlo engine is vectorized with NumPy to keep the app responsive even with thousands of simulations.

---

## 📌 Possíveis extensões futuras

- Dashboard de risco mais completo (aba **Risk Dashboard**).
- Fronteira eficiente e otimização de portfólio.
- Suporte a diferentes horizontes de tempo e frequências (diário, semanal, mensal).
- Exportar resultados em CSV/Excel.

# portfolio-risk-simulator
Interactive portfolio risk simulator with Monte Carlo analysis, volatility modeling and risk metrics (VaR, drawdown, expected return).


app
User Input
   ↓
Download Data
   ↓
Compute Returns & Covariance
   ↓
Monte Carlo Simulation
   ↓
Risk Metrics
   ↓
Interactive Graphs