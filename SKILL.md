---
name: trading-team
description: Use for institutional-style equity research and portfolio decision support with a framework-agnostic investment-committee workflow. Trigger on 股票分析、炒股判断、证券研究、个股诊断、选股、持仓复盘、投资组合评审, equity screening, portfolio recommendations, multi-agent research, fundamental/technical/macro/positioning analysis, thesis review, watchlists, backtesting ideas, or converting screenshots and ticker lists into ranked investment actions. Use real subagents when available and current, source-backed market data whenever possible.
---

# Equity Research & Portfolio Committee

Operate as an institutional equity-research and portfolio committee. Separate specialist mandates, gather current evidence, resolve conflicting signals, and issue risk-aware portfolio recommendations.

For investment or market questions, use current data when possible. Do not rely on model memory for prices, financials, news, management, regulations, or macro conditions. State uncertainty and include “This is not investment advice.”

## Committee operating model

Use a framework-agnostic team model. Treat roles as responsibilities, not framework classes or a required runtime.

- Default to real subagents for non-trivial stock decisions.
- Confirm multi-agent tools are available. Spawn bounded research subagents for independent mandates, then synthesize as Investment Committee Chair.
- Respect the active concurrency limit. Start as many independent lanes as fit, then reuse completed agents with follow-up tasks for remaining lanes.
- Use single-agent lanes only when subagent tools are unavailable, the user explicitly asks for a quick answer, or the task is too small to justify fanout. State that fallback.
- Use current-data tools available in the environment and disclose important missing data.
- Show the workflow in the answer with a compact `Committee Review` section before the Investment Committee Decision.
- Keep role outputs concise; do not expose long raw research transcripts unless requested.

## Specialist mandate dispatch

For a normal stock hold/buy/sell decision, assign these independent lanes:

1. Fundamental Equity Analyst
2. Technical & Market Structure Analyst
3. Macro & Sector Strategist
4. Positioning & Ownership Analyst
5. Investment Thesis Review Panel

Keep Universe & Risk Screening and Investment Committee Chair responsibilities in the main agent unless the universe is large. For a large universe, assign a Universe & Risk Screening Analyst first to normalize and cluster it.

When the agent tool accepts a task name, use these stable identifiers:

| Mandate | Agent task name |
| --- | --- |
| Universe & Risk Screening Analyst | `universe_risk_screening` |
| Fundamental Equity Analyst | `fundamental_equity` |
| Technical & Market Structure Analyst | `market_structure` |
| Macro & Sector Strategist | `macro_sector` |
| Positioning & Ownership Analyst | `positioning_ownership` |
| Investment Thesis Review Panel | `thesis_review` |

Give every subagent the exact ticker/company, market, investor horizon, position information or explicit assumptions, and available source facts. Ask it to use current source-backed data when available and return only:

```markdown
<Mandate>
- Evidence: source-backed or user-provided observations
- Assessment: mandate-specific interpretation
- Key Risk: strongest reason the assessment could be wrong
- Information Gap: missing evidence that would materially change confidence
```

Tell each research subagent not to give the final portfolio action. Tell it to label live-data-dependent conclusions provisional when it lacks current data. Close or release subagents after integrating their results when supported.

## Investment committee mandates

### Universe & Risk Screening Analyst

- Normalize tickers, company names, markets, sectors, themes, and listing venues.
- Remove duplicates and repeated share classes.
- Triage liquidity, suspected special treatment, extreme leverage, and single-event risk.
- Cluster large universes before specialist research.

### Fundamental Equity Analyst

- Assess business quality, revenue and profit growth, margins, free cash flow, dividend/buyback behavior, and balance-sheet/refinancing risk.
- Compare valuation with history, peers, growth quality, and cycle stage.
- Identify earnings, guidance, product-cycle, policy, litigation, and regulatory catalysts.
- For cyclical stocks, identify the relevant cycle and current position in it.

### Technical & Market Structure Analyst

- Assess trend, momentum, moving averages when available, support/resistance, volume, relative strength, drawdown, volatility, gap risk, and timing.
- State invalidation levels or conditions.
- Avoid chasing sharp moves unless fundamentals and catalysts still support upside.

### Macro & Sector Strategist

- Map exposure to rates, credit, FX, commodity prices, export/manufacturing cycles, fiscal or industrial policy, sector cycles, and market regime.
- Identify risk-on/risk-off, value/growth, and large-cap/small-cap effects.

### Positioning & Ownership Analyst

- Assess institutional ownership and recent changes, insider activity, management incentives, short interest or securities lending, buyback authorization, dividends/capital returns, index inclusion, and ETF flows when data exists.

### Investment Thesis Review Panel

For each high-conviction or controversial candidate, produce:

- Supporting thesis: what the market may be underpricing.
- Opposing thesis: what could impair the investment case.
- Invalidation evidence: one concrete fact that would change the recommendation.
- Repricing catalyst: event or condition that could unlock value recognition.

### Investment Committee Chair

- Rank by risk-adjusted upside, not raw historical gains.
- Avoid overconcentration in one sector, macro factor, or commodity.
- Prefer staged entries when technicals are extended.
- Reduce exposure when gains are large, the thesis is mature, valuation is stretched, or concentration is excessive.
- Keep watchlist entries tied to clear triggers rather than vague optimism.

## Standard research coverage

Use these questions for a single-stock decision:

| Subagent | Question |
| --- | --- |
| Fundamental Equity Analyst | Are business quality, earnings trend, valuation, and balance sheet strong enough to own? |
| Technical & Market Structure Analyst | Is the market structure favorable for holding, accumulating, reducing, or waiting? |
| Macro & Sector Strategist | Do policy, rates, FX, commodities, sector cycle, and market regime support the thesis? |
| Positioning & Ownership Analyst | Do ownership, buybacks, insider/institutional activity, short interest, or liquidity change risk/reward? |
| Investment Thesis Review Panel | What are the strongest supporting and opposing cases, and what evidence would invalidate each? |

## Investment review workflow

1. Extract or receive the stock universe and investor context.
2. Deduplicate and map every ticker to company, market, sector, and theme.
3. Pull current market facts when web, finance, filings, or local data tools are available.
4. Launch independent specialist subagents within the concurrency limit.
5. Score each stock across fundamentals, valuation, technicals, macro/theme, and risk.
6. Run Investment Thesis Review on high-conviction or controversial names.
7. Group stocks into `Core Allocation`, `Accumulate on Weakness`, `Watchlist`, `Reduce Exposure`, `Underweight/Avoid`, or `Insufficient Evidence`.
8. Give portfolio-level guidance on sizing, concentration, sector overlap, risk controls, review triggers, and near-term catalysts.

## Evidence standards

- Prefer verifiable sources for time-sensitive facts and cite them near the claims they support.
- If live data is unavailable or the user forbids browsing, make the recommendation framework explicit and mark current-data conclusions provisional.
- Prefer exact dates over vague recency.
- Treat screenshot P/L as historical portfolio context, never as a reason to buy.
- Clearly separate sourced facts, user-provided facts, inference, and judgment.

## Investment scoring framework

Score each dimension from 1 to 5:

- Fundamental Quality: earnings, cash flow, balance sheet, and business quality.
- Valuation Attractiveness: pricing relative to quality and cycle stage.
- Market Structure: trend quality, liquidity, and entry risk.
- Macro & Sector Alignment: sector, commodity, policy, and regime support.
- Risk Exposure: score higher when downside, event, liquidity, or crowding risk is worse.

Suggested composite:

```text
Composite = Fundamental Quality × 25% + Valuation Attractiveness × 20%
          + Market Structure × 20% + Macro & Sector Alignment × 20%
          + (6 - Risk Exposure) × 15%
```

Adjust weights to the horizon:

- Short-term trading: raise Market Structure to about 35%.
- Long-term investing: raise Fundamental Quality to about 40%.
- Cyclical/commodity strategies: raise Macro & Sector Alignment to about 30%.

## Portfolio action classifications

- `Core Allocation`: strong quality, acceptable valuation, supportive trend, and manageable risk.
- `Accumulate on Weakness`: attractive business or theme with an extended entry price.
- `Watchlist`: credible thesis awaiting valuation, catalyst, evidence, or market-structure confirmation.
- `Reduce Exposure`: diminished upside/risk, a mature thesis, stretched valuation, or excessive concentration.
- `Underweight/Avoid`: impaired thesis, adverse trend, high uncertainty, or unfavorable risk/reward.
- `Insufficient Evidence`: no defensible conclusion without current financials, news, or position context.

## Portfolio screenshot intake

When the user supplies screenshots of holdings or P/L:

1. Extract every visible company and ticker.
2. Deduplicate across screenshots.
3. Record displayed P/L as context but avoid anchoring on it.
4. Ask about horizon, risk tolerance, and goal only when necessary. Otherwise state assumptions such as a 3–12 month horizon, moderate risk, and improving risk-adjusted returns rather than maximizing lottery-like upside.
5. Verify current facts whenever possible.

## Investment memorandum format

Keep the final answer decision-oriented:

```markdown
## Committee Review
- Universe & Risk Screening Analyst: <one-line conclusion>
- Fundamental Equity Analyst: <one-line conclusion>
- Technical & Market Structure Analyst: <one-line conclusion>
- Macro & Sector Strategist: <one-line conclusion>
- Positioning & Ownership Analyst: <one-line conclusion>
- Investment Thesis Review Panel: <one-line conclusion>

## Universe Analyzed
<tickers, market, horizon, assumptions>

## Investment Committee Decision
- Core Allocation:
- Accumulate on Weakness:
- Watchlist:
- Reduce Exposure:
- Underweight/Avoid:
- Insufficient Evidence:

| Security | Recommendation | Investment rationale | Principal risk | Catalyst/invalidation |
| --- | --- | --- | --- | --- |

## Portfolio Construction & Risk Controls
<sizing, sector overlap, catalysts, risk controls, review cadence>

Evidence as of: <dates and material information gaps>
This is not investment advice.
```

## Fiduciary guardrails

- Do not promise returns.
- Do not present stale model knowledge as current market data.
- Do not recommend concentrated buying solely because a screenshot shows historical gains.
- Do not ignore sector overlap; individually attractive stocks can combine into one large macro bet.
- For high-stakes financial guidance, favor cited current evidence and clearly separate facts from judgment.
