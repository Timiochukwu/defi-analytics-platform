'use client'

import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'
import { Coins, TrendingUp, Shield, Zap, AlertCircle, RefreshCw, Download, Settings, Wallet } from 'lucide-react'

export default function DeFiDashboard() {
  const [defiData, setDefiData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [selectedProtocol, setSelectedProtocol] = useState('all')

  useEffect(() => {
    fetchDefiData()
  }, [selectedProtocol])

  const fetchDefiData = async () => {
    setLoading(true)
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      setDefiData(getMockData())
    } catch (error) {
      console.error('Error fetching DeFi data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getMockData = () => ({
    total_tvl: 4520000,
    total_yield: 187500,
    avg_apy: 12.4,
    protocols: [
      { name: 'Aave', tvl: 2100000, apy: 8.5, risk_score: 92 },
      { name: 'Compound', tvl: 1500000, apy: 7.2, risk_score: 90 },
      { name: 'Uniswap V3', tvl: 920000, apy: 18.3, risk_score: 85 }
    ],
    yield_opportunities: [
      { protocol: 'Aave USDC', apy: 8.5, tvl: 1200000, risk: 'Low', category: 'Lending' },
      { protocol: 'Compound DAI', apy: 7.2, tvl: 950000, risk: 'Low', category: 'Lending' },
      { protocol: 'Uniswap ETH/USDC', apy: 18.3, tvl: 650000, risk: 'Medium', category: 'LP' },
      { protocol: 'Curve 3Pool', apy: 12.1, tvl: 450000, risk: 'Low', category: 'LP' },
      { protocol: 'Yearn USDT', apy: 9.8, tvl: 270000, risk: 'Medium', category: 'Vault' }
    ],
    impermanent_loss: {
      current: -2.3,
      scenarios: [
        { price_change: -50, il: -5.7 },
        { price_change: -25, il: -2.0 },
        { price_change: 0, il: 0 },
        { price_change: 25, il: -2.0 },
        { price_change: 50, il: -5.7 },
        { price_change: 100, il: -13.4 }
      ]
    },
    smart_contract_risks: [
      { protocol: 'Aave', audit_score: 95, time_score: 100, tvl_score: 98, total: 92 },
      { protocol: 'Compound', audit_score: 93, time_score: 100, tvl_score: 95, total: 90 },
      { protocol: 'Uniswap', audit_score: 90, time_score: 95, tvl_score: 90, total: 85 }
    ],
    apy_history: Array.from({ length: 30 }, (_, i) => ({
      day: `Day ${i + 1}`,
      aave: 8.5 + (Math.random() - 0.5) * 2,
      compound: 7.2 + (Math.random() - 0.5) * 1.5,
      uniswap: 18.3 + (Math.random() - 0.5) * 4
    }))
  })

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-12 w-12 animate-spin text-purple-600 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Loading DeFi data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg">
                <Coins className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  DeFi Analytics
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">Protocol Analysis & Yield Optimization</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2">
                <Wallet className="h-4 w-4" />
                Connect Wallet
              </button>
              <button onClick={fetchDefiData} className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors flex items-center gap-2">
                <RefreshCw className="h-4 w-4" />
                Refresh
              </button>
              <button className="p-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Total Value Locked"
            value={`$${(defiData.total_tvl / 1000000).toFixed(2)}M`}
            change="+15.2%"
            isPositive={true}
            icon={<Coins className="h-5 w-5" />}
            gradient="from-purple-500 to-purple-600"
          />
          <MetricCard
            title="Total Yield Earned"
            value={`$${defiData.total_yield.toLocaleString()}`}
            subtitle="30-day"
            isPositive={true}
            icon={<TrendingUp className="h-5 w-5" />}
            gradient="from-green-500 to-green-600"
          />
          <MetricCard
            title="Average APY"
            value={`${defiData.avg_apy}%`}
            subtitle="Across all protocols"
            icon={<Zap className="h-5 w-5" />}
            gradient="from-yellow-500 to-orange-500"
          />
          <MetricCard
            title="Risk Score"
            value="88/100"
            subtitle="Portfolio avg"
            isPositive={true}
            icon={<Shield className="h-5 w-5" />}
            gradient="from-blue-500 to-blue-600"
          />
        </div>

        {/* Yield Opportunities */}
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Top Yield Opportunities</h2>
            <select className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700">
              <option>All Categories</option>
              <option>Lending</option>
              <option>Liquidity Pools</option>
              <option>Vaults</option>
            </select>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600 dark:text-gray-400">Protocol</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-600 dark:text-gray-400">APY</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-600 dark:text-gray-400">TVL</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-600 dark:text-gray-400">Risk</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-600 dark:text-gray-400">Category</th>
                </tr>
              </thead>
              <tbody>
                {defiData.yield_opportunities.map((opp: any, idx: number) => (
                  <tr key={idx} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                    <td className="py-4 px-4 font-medium text-gray-900 dark:text-white">{opp.protocol}</td>
                    <td className="py-4 px-4 text-right">
                      <span className="text-green-600 dark:text-green-400 font-semibold">{opp.apy}%</span>
                    </td>
                    <td className="py-4 px-4 text-right text-gray-700 dark:text-gray-300">
                      ${(opp.tvl / 1000).toFixed(0)}K
                    </td>
                    <td className="py-4 px-4 text-center">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        opp.risk === 'Low' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                        opp.risk === 'Medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                        'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                      }`}>
                        {opp.risk}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-center text-sm text-gray-600 dark:text-gray-400">{opp.category}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* APY History */}
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">APY Trends (30 Days)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={defiData.apy_history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="aave" stroke="#8b5cf6" strokeWidth={2} name="Aave" />
                <Line type="monotone" dataKey="compound" stroke="#3b82f6" strokeWidth={2} name="Compound" />
                <Line type="monotone" dataKey="uniswap" stroke="#ec4899" strokeWidth={2} name="Uniswap" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Smart Contract Risk */}
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Smart Contract Risk Analysis</h2>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={defiData.smart_contract_risks}>
                <PolarGrid />
                <PolarAngleAxis dataKey="protocol" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar name="Audit Score" dataKey="audit_score" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.6} />
                <Radar name="Time Score" dataKey="time_score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
                <Radar name="TVL Score" dataKey="tvl_score" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
                <Tooltip />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Impermanent Loss Calculator */}
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-2 mb-6">
            <AlertCircle className="h-5 w-5 text-yellow-600" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Impermanent Loss Calculator</h2>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-4">
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Current Impermanent Loss</div>
                <div className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">
                  {defiData.impermanent_loss.current}%
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                  Based on current price movement
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Initial Price:</span>
                  <span className="font-medium text-gray-900 dark:text-white">$2,000</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Current Price:</span>
                  <span className="font-medium text-gray-900 dark:text-white">$2,100</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Price Change:</span>
                  <span className="font-medium text-green-600">+5.0%</span>
                </div>
              </div>
            </div>
            <div>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={defiData.impermanent_loss.scenarios}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="price_change" label={{ value: 'Price Change (%)', position: 'insideBottom', offset: -5 }} />
                  <YAxis label={{ value: 'IL (%)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="il" stroke="#f59e0b" strokeWidth={3} dot={{ fill: '#f59e0b', r: 5 }} />
                </LineChart>
              </ResponsiveContainer>
              <p className="text-xs text-gray-500 dark:text-gray-500 text-center mt-2">
                Impermanent loss increases with price divergence
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

function MetricCard({ title, value, subtitle, change, isPositive, icon, gradient }: any) {
  return (
    <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-start justify-between mb-4">
        <div className={`p-2 rounded-lg bg-gradient-to-r ${gradient}`}>
          <div className="text-white">{icon}</div>
        </div>
        {change && (
          <span className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {change}
          </span>
        )}
      </div>
      <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">{title}</div>
      <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">{value}</div>
      {subtitle && <div className="text-xs text-gray-500 dark:text-gray-500">{subtitle}</div>}
    </div>
  )
}
