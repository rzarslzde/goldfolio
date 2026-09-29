import { useMemo, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const assetOptions = [
  { value: '18k_gram', label: '18k gram' },
  { value: 'half_coin', label: 'half coin' },
  { value: 'quarter_coin', label: 'quarter coin' },
  { value: 'bahar_coin', label: 'bahar coin' },
]

function App() {
  const [token, setToken] = useState('')
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('admin123')
  const [prices, setPrices] = useState({ gram_18k: 0, half_coin: 0, quarter_coin: 0, bahar_coin: 0 })
  const [holdings, setHoldings] = useState([])
  const [summary, setSummary] = useState({ total_irt: 0, by_asset: {} })
  const [form, setForm] = useState({ asset_type: '18k_gram', quantity: 0 })
  const [editingId, setEditingId] = useState(null)

  const authHeaders = useMemo(() => ({
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }), [token])

  async function login(e) {
    e.preventDefault()
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    if (!res.ok) return alert('Login failed')
    const data = await res.json()
    setToken(data.access_token)
  }

  async function loadAll() {
    const [p, h, s] = await Promise.all([
      fetch(`${API_BASE}/portfolio/prices`, { headers: authHeaders }),
      fetch(`${API_BASE}/portfolio/holdings`, { headers: authHeaders }),
      fetch(`${API_BASE}/portfolio/summary`, { headers: authHeaders }),
    ])

    if (p.ok) setPrices(await p.json())
    if (h.ok) setHoldings(await h.json())
    if (s.ok) setSummary(await s.json())
  }

  async function savePrices(e) {
    e.preventDefault()
    const res = await fetch(`${API_BASE}/portfolio/prices`, {
      method: 'PUT',
      headers: authHeaders,
      body: JSON.stringify({
        gram_18k: Number(prices.gram_18k || 0),
        half_coin: Number(prices.half_coin || 0),
        quarter_coin: Number(prices.quarter_coin || 0),
        bahar_coin: Number(prices.bahar_coin || 0),
      }),
    })
    if (!res.ok) return alert('Failed to save prices')
    await loadAll()
  }

  async function saveHolding(e) {
    e.preventDefault()
    const payload = { asset_type: form.asset_type, quantity: Number(form.quantity || 0) }

    const endpoint = editingId
      ? `${API_BASE}/portfolio/holdings/${editingId}`
      : `${API_BASE}/portfolio/holdings`

    const method = editingId ? 'PUT' : 'POST'
    const res = await fetch(endpoint, {
      method,
      headers: authHeaders,
      body: JSON.stringify(payload),
    })

    if (!res.ok) return alert('Failed to save holding')
    setForm({ asset_type: '18k_gram', quantity: 0 })
    setEditingId(null)
    await loadAll()
  }

  async function removeHolding(id) {
    const res = await fetch(`${API_BASE}/portfolio/holdings/${id}`, {
      method: 'DELETE',
      headers: authHeaders,
    })
    if (!res.ok) return alert('Failed to remove holding')
    await loadAll()
  }

  function startEdit(item) {
    setEditingId(item.id)
    setForm({ asset_type: item.asset_type, quantity: item.quantity })
  }

  return (
    <div className="container">
      <h1>Goldfolio (IRT)</h1>

      {!token ? (
        <form onSubmit={login} className="card">
          <h2>Login</h2>
          <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" />
          <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
          <button type="submit">Sign in</button>
        </form>
      ) : (
        <>
          <div className="row">
            <button onClick={loadAll}>Refresh data</button>
          </div>

          <form onSubmit={savePrices} className="card">
            <h2>Current Prices (IRT)</h2>
            <label>18k gram<input type="number" value={prices.gram_18k} onChange={(e) => setPrices({ ...prices, gram_18k: e.target.value })} /></label>
            <label>half coin<input type="number" value={prices.half_coin} onChange={(e) => setPrices({ ...prices, half_coin: e.target.value })} /></label>
            <label>quarter coin<input type="number" value={prices.quarter_coin} onChange={(e) => setPrices({ ...prices, quarter_coin: e.target.value })} /></label>
            <label>bahar coin<input type="number" value={prices.bahar_coin} onChange={(e) => setPrices({ ...prices, bahar_coin: e.target.value })} /></label>
            <button type="submit">Save prices</button>
          </form>

          <form onSubmit={saveHolding} className="card">
            <h2>{editingId ? 'Edit Holding' : 'Add Holding'}</h2>
            <label>Asset
              <select value={form.asset_type} onChange={(e) => setForm({ ...form, asset_type: e.target.value })}>
                {assetOptions.map((opt) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
              </select>
            </label>
            <label>Quantity<input type="number" step="0.01" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} /></label>
            <button type="submit">{editingId ? 'Update' : 'Add'}</button>
          </form>

          <div className="card">
            <h2>Holdings</h2>
            <table>
              <thead>
                <tr><th>ID</th><th>Asset</th><th>Qty</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {holdings.map((h) => (
                  <tr key={h.id}>
                    <td>{h.id}</td>
                    <td>{h.asset_type}</td>
                    <td>{h.quantity}</td>
                    <td>
                      <button onClick={() => startEdit(h)}>Edit</button>
                      <button onClick={() => removeHolding(h.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="card">
            <h2>Portfolio Value (IRT)</h2>
            <p><strong>Total:</strong> {Number(summary.total_irt || 0).toLocaleString('en-US')} Toman</p>
            <ul>
              <li>18k gram: {Number(summary.by_asset?.['18k_gram'] || 0).toLocaleString('en-US')}</li>
              <li>half coin: {Number(summary.by_asset?.half_coin || 0).toLocaleString('en-US')}</li>
              <li>quarter coin: {Number(summary.by_asset?.quarter_coin || 0).toLocaleString('en-US')}</li>
              <li>bahar coin: {Number(summary.by_asset?.bahar_coin || 0).toLocaleString('en-US')}</li>
            </ul>
          </div>
        </>
      )}
    </div>
  )
}

export default App
