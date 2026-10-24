import { useEffect, useState } from 'react'

const API = 'http://127.0.0.1:5000'

function AdminDashboard() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadBookings() {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API}/api/bookings`)
      const data = await response.json()
      if (!response.ok) throw new Error(data.message || 'Could not load bookings.')
      setBookings(data)
    } catch (err) {
      setError(`${err.message} Check that the backend is running and MongoDB is connected.`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadBookings() }, [])

  return (
    <div className="admin-page">
      <header className="admin-header">
        <a className="brand" href="/"><span className="brand-mark">H</span><span>Hotel<span className="brand-light">Pro</span></span></a>
        <a className="back-link" href="/">← Back to website</a>
      </header>
      <main className="admin-main">
        <p className="eyebrow">HOTEL MANAGEMENT</p>
        <div className="admin-title-row"><div><h1>Booking <em>dashboard.</em></h1><p>Review the booking requests saved in your database.</p></div><button className="refresh-button" onClick={loadBookings}>↻ Refresh</button></div>
        <div className="stats-row"><div className="stat-card"><span>TOTAL BOOKINGS</span><strong>{bookings.length}</strong></div><div className="stat-card"><span>PENDING REQUESTS</span><strong>{bookings.filter(b => b.status === 'Pending').length}</strong></div><div className="stat-card"><span>CONFIRMED</span><strong>{bookings.filter(b => b.status === 'Confirmed').length}</strong></div></div>
        {loading && <p className="notice">Loading bookings…</p>}
        {error && <div className="error-panel"><strong>Unable to load bookings</strong><p>{error}</p><button className="refresh-button" onClick={loadBookings}>Try again</button></div>}
        {!loading && !error && <div className="table-wrap"><table><thead><tr><th>Guest</th><th>Room</th><th>Price / night</th><th>Check-in</th><th>Check-out</th><th>Status</th></tr></thead><tbody>
          {bookings.map(b => <tr key={b._id}><td><strong>{b.guestName}</strong></td><td>{b.roomName}</td><td>₹{Number(b.roomPrice).toLocaleString('en-IN')}</td><td>{b.checkIn ? new Date(b.checkIn).toLocaleDateString('en-IN') : '—'}</td><td>{b.checkOut ? new Date(b.checkOut).toLocaleDateString('en-IN') : '—'}</td><td><span className={`status status-${String(b.status).toLowerCase()}`}>{b.status}</span></td></tr>)}
          {bookings.length === 0 && <tr><td className="empty-cell" colSpan="6">No bookings yet. Submit a booking from the home page to see it here.</td></tr>}
        </tbody></table></div>}
      </main>
      <footer><a href="/">← Return to HotelPro</a><span>Private demo dashboard · Add authentication before public deployment.</span></footer>
    </div>
  )
}

export default AdminDashboard
