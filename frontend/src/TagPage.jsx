import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import './TagPage.css'

const MEMBER_KEY = 'kajilog_member_id'

function TagPage() {
  const { tagId } = useParams()
  const [tagInfo, setTagInfo] = useState(null)
  const [record, setRecord] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    fetch(`/api/tags/${tagId}`)
      .then((res) => {
        if (!res.ok) throw new Error('tag not found')
        return res.json()
      })
      .then((data) => {
        if (cancelled) return
        setTagInfo(data)
        const savedMemberId = localStorage.getItem(MEMBER_KEY)
        const savedMember = data.members.find((m) => m.id === savedMemberId)
        if (savedMember) {
          recordAs(data, savedMember)
        } else {
          setLoading(false)
        }
      })
      .catch(() => {
        if (!cancelled) {
          setError('タグが見つかりませんでした')
          setLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tagId])

  function recordAs(info, member) {
    setLoading(true)
    fetch('/api/records', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tag_id: info.tag_id, member_id: member.id }),
    })
      .then((res) => {
        if (!res.ok) throw new Error('record failed')
        return res.json()
      })
      .then((data) => {
        localStorage.setItem(MEMBER_KEY, member.id)
        setRecord({ ...data, member })
        setLoading(false)
      })
      .catch(() => {
        setError('記録に失敗しました')
        setLoading(false)
      })
  }

  function undo() {
    if (!record) return
    fetch(`/api/records/${record.record_id}/undo`, { method: 'POST' }).then(() => {
      setRecord((prev) => ({ ...prev, undone: true }))
    })
  }

  function changeMember() {
    localStorage.removeItem(MEMBER_KEY)
    setRecord(null)
  }

  if (loading) {
    return (
      <main className="tag-page">
        <p>読み込み中...</p>
      </main>
    )
  }

  if (error) {
    return (
      <main className="tag-page">
        <p>{error}</p>
      </main>
    )
  }

  if (record) {
    return (
      <main className="tag-page">
        {record.undone ? (
          <p>取り消しました</p>
        ) : (
          <>
            <p className="confirmation">
              ✅ {record.chore_name}を記録しました（{record.member.name}）
            </p>
            <button type="button" onClick={undo}>
              取り消す
            </button>
          </>
        )}
        <button type="button" className="change-member" onClick={changeMember}>
          自分じゃない場合はこちら
        </button>
      </main>
    )
  }

  return (
    <main className="tag-page">
      <p>{tagInfo.chore.name} — 誰がやりましたか？</p>
      <div className="member-buttons">
        {tagInfo.members.map((m) => (
          <button
            key={m.id}
            type="button"
            className="member-button"
            style={{ backgroundColor: m.color || '#888' }}
            onClick={() => recordAs(tagInfo, m)}
          >
            <span className="icon">{m.icon}</span>
            {m.name}
          </button>
        ))}
      </div>
    </main>
  )
}

export default TagPage
