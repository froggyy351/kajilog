import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [members, setMembers] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/dashboard')
      .then((res) => {
        if (!res.ok) throw new Error('failed to load dashboard')
        return res.json()
      })
      .then((data) => setMembers(data.members))
      .catch(() => setError('データの取得に失敗しました'))
  }, [])

  const maxPoints = members ? Math.max(1, ...members.map((m) => m.total_points)) : 1

  return (
    <main className="home">
      <h1>カジログ</h1>
      <p className="subtitle">家事実績をNFCタップで記録・可視化するアプリ</p>

      {error && <p className="error">{error}</p>}

      {members && (
        <div className="dashboard">
          {members.map((m) => (
            <div className="bar-row" key={m.id}>
              <span className="member-label">
                {m.icon} {m.name}
              </span>
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{
                    width: `${(m.total_points / maxPoints) * 100}%`,
                    backgroundColor: m.color || '#888',
                  }}
                />
              </div>
              <span className="bar-value">{m.total_points}pt</span>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}

export default App
