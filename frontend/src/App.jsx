import { useState } from 'react'
import AdminDashboard from './AdminDashboard.jsx'

const API = 'http://127.0.0.1:5000'

const rooms = [
  { id: 1, name: 'Standard Room', price: 1500, tag: 'Comfort made simple', symbol: '☀', description: 'A welcoming space with the essentials for a restful stay.' },
  { id: 2, name: 'Deluxe Room', price: 2500, tag: 'A little more room', symbol: '✦', description: 'More space, extra comfort, and a calm atmosphere.' },
  { id: 3, name: 'Luxury Suite', price: 4000, tag: 'Your special escape', symbol: '❋', description: 'A spacious suite designed for a memorable visit.' }
]

function App() {
  const [selectedRoom, setSelectedRoom] = useState(rooms[0])
  const [guestName, setGuestName] = useState('')
  const [checkIn, setCheckIn] = useState('')
  const [checkOut, setCheckOut] = useState('')
  const [message, setMessage] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if (window.location.pathname === '/admin') return <AdminDashboard />

  async function handleBooking(event) {
    event.preventDefault()
    setMessage('')
    if (!guestName.trim() || !checkIn || !checkOut) {
      setMessage('Please fill in all fields.')
      return
    }
    if (new Date(checkOut) <= new Date(checkIn)) {
      setMessage('Check-out must be after check-in.')
      return
    }

    setSubmitting(true)
    try {
      const response = await fetch(`${API}/api/bookings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          guestName: guestName.trim(),
          roomName: selectedRoom.name,
          roomPrice: selectedRoom.price,
          checkIn,
          checkOut
        })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.message || 'Booking could not be saved.')
      setMessage('Your booking request has been saved! Status: Pending.')
      setGuestName('')
      setCheckIn('')
      setCheckOut('')
    } catch (error) {
      setMessage(`${error.message} Make sure the backend is running.`)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="site-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="HotelPro home">
          <span className="brand-mark">H</span>
          <span>Hotel<span className="brand-light">Pro</span></span>
        </a>
        <nav>
          <a href="#rooms">Rooms</a>
          <a href="#booking">Book a stay</a>
          <a className="admin-link" href="/admin">Admin</a>
        </nav>
      </header>

      <main>
        <section className="hero">
          <div className="hero-copy">
            <p className="eyebrow"><span></span> YOUR STAY, MADE SPECIAL</p>
            <h1>Find your place<br />to <em>feel at home.</em></h1>
            <p className="hero-text">Thoughtful rooms, warm hospitality, and a smoother way to plan your next stay.</p>
            <a className="primary-button" href="#rooms">Explore rooms <span>↗</span></a>
            <div className="hero-note"><span className="note-star">✦</span><span><strong>Simple booking.</strong><br />Comfortable stays.</span></div>
          </div>
          <div className="hero-art" role="img" aria-label="Illustration of a peaceful hotel room">
            <div className="sun"></div>
            <div className="art-label">A PLACE TO UNWIND</div>
            <div className="window"><div className="window-view"></div><div className="window-line"></div></div>
            <div className="plant"><i></i><i></i><i></i><b></b></div>
            <div className="bed"><div className="headboard"></div><div className="pillow p1"></div><div className="pillow p2"></div><div className="duvet"></div><div className="bed-foot"></div></div>
            <div className="side-table"><div></div></div>
            <div className="art-caption">REST • RESET • REPEAT</div>
          </div>
        </section>

        <section className="intro-strip">
          <div><span className="strip-icon">✧</span><p><strong>Comfort first</strong><small>Rooms for every kind of trip</small></p></div>
          <div><span className="strip-icon">⌁</span><p><strong>Easy booking</strong><small>A simple booking experience</small></p></div>
          <div><span className="strip-icon">♡</span><p><strong>Stay your way</strong><small>Choose the room that fits you</small></p></div>
        </section>

        <section id="rooms" className="rooms-section">
          <div className="section-heading">
            <div><p className="eyebrow">CHOOSE YOUR SPACE</p><h2>Rooms made for <em>you.</em></h2></div>
            <p>From a quick getaway to a little luxury, find the right fit for your stay.</p>
          </div>
          <div className="room-grid">
            {rooms.map((room, index) => (
              <article className={`room-card ${selectedRoom.id === room.id ? 'selected' : ''}`} key={room.id}>
                <div className={`room-art room-art-${index + 1}`}>
                  <span className="room-number">0{index + 1}</span>
                  <div className="mini-window"></div><div className="mini-bed"><span></span><i></i></div><div className="mini-plant">♣</div>
                  <span className="room-symbol">{room.symbol}</span>
                </div>
                <div className="room-info">
                  <p className="room-tag">{room.tag}</p><h3>{room.name}</h3><p className="room-description">{room.description}</p>
                  <div className="room-bottom"><p><strong>₹{room.price.toLocaleString('en-IN')}</strong><span> / night</span></p>
                    <button type="button" className={selectedRoom.id === room.id ? 'choose-button chosen' : 'choose-button'} onClick={() => { setSelectedRoom(room); setMessage('') }}>
                      {selectedRoom.id === room.id ? 'Selected ✓' : 'Choose room'}
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section id="booking" className="booking-section">
          <div className="booking-copy"><p className="eyebrow">LET'S PLAN YOUR STAY</p><h2>Your next stay<br />starts <em>right here.</em></h2><p>Enter your details and send a booking request. You can view saved requests in the admin dashboard.</p><div className="selected-room"><span>YOUR ROOM</span><strong>{selectedRoom.name}</strong><b>₹{selectedRoom.price.toLocaleString('en-IN')} <small>/ night</small></b></div></div>
          <form className="booking-form" onSubmit={handleBooking}>
            <h3>Make a booking</h3><p className="form-subtitle">A few details and you're all set.</p>
            <label>Guest name<input value={guestName} onChange={(e) => setGuestName(e.target.value)} placeholder="Enter your full name" required /></label>
            <div className="date-row"><label>Check-in<input type="date" value={checkIn} onChange={(e) => setCheckIn(e.target.value)} required /></label><label>Check-out<input type="date" value={checkOut} onChange={(e) => setCheckOut(e.target.value)} required /></label></div>
            <div className="form-room"><span>Selected room</span><strong>{selectedRoom.name}</strong><b>₹{selectedRoom.price.toLocaleString('en-IN')} / night</b></div>
            <button className="submit-button" disabled={submitting} type="submit">{submitting ? 'Sending request…' : 'Request booking'} <span>→</span></button>
            {message && <p className={message.includes('saved') ? 'form-message success' : 'form-message'} role="status">{message}</p>}
            <p className="form-footnote">Booking requests are saved with Pending status.</p>
          </form>
        </section>
      </main>

      <footer><a className="brand footer-brand" href="/"><span className="brand-mark">H</span><span>Hotel<span className="brand-light">Pro</span></span></a><span>Made for a more comfortable stay.</span><a href="/admin">Admin dashboard ↗</a></footer>
    </div>
  )
}

export default App
