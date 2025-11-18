# 🪙 DeFi Analytics - Frontend Dashboard

Professional React dashboard for the DeFi Analytics Platform.

## Features

- ✅ Protocol analysis (Aave, Compound, Uniswap)
- ✅ Top yield opportunities comparison
- ✅ APY trend tracking (30-day history)
- ✅ Smart contract risk analysis (radar chart)
- ✅ Impermanent loss calculator
- ✅ Wallet connection (Web3)
- ✅ Dark/Light mode
- ✅ Mobile responsive

## Quick Start

```bash
cd defi-analytics-platform/frontend
npm install
npm run dev
```

Open [http://localhost:3001](http://localhost:3001)

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Recharts
- ethers.js (Web3)
- SWR

## API Connection

Configure in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
```

The dashboard connects to the FastAPI backend running on port 8001.

## Dashboard Sections

1. **Key Metrics** - TVL, Total Yield, Average APY, Risk Score
2. **Yield Opportunities** - Top 5 protocols with APY comparison
3. **APY Trends** - 30-day historical APY for major protocols
4. **Smart Contract Risk** - Radar chart showing audit, time, and TVL scores
5. **Impermanent Loss** - Calculator with price change scenarios

## Deploy

```bash
npm run build
npm start
```

Or deploy to Vercel:
```bash
vercel
```
