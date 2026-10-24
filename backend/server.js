require('dotenv').config();
const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const Booking = require('./models/Booking')

const app = express()
const PORT = Number(process.env.PORT) || 5000

app.use(cors({ origin: true }))
app.use(express.json())

const rooms = [
  { id: 1, name: 'Standard Room', price: 1500, description: 'A comfortable room for a relaxing stay.', features: ['Wi-Fi', 'Air conditioning', 'Queen bed'] },
  { id: 2, name: 'Deluxe Room', price: 2500, description: 'Extra space and comfort for your visit.', features: ['Wi-Fi', 'Air conditioning', 'King bed'] },
  { id: 3, name: 'Luxury Suite', price: 4000, description: 'A spacious suite for a special stay.', features: ['Wi-Fi', 'Living area', 'King bed'] }
]

app.get('/', (_req, res) => {
  res.status(200).send('HotelPro Backend is running!')
})

app.get('/test', (_req, res) => {
  res.status(200).send('Test route is working!')
})

app.get('/api/rooms', (_req, res) => {
  res.json(rooms)
})

app.get('/api/bookings', async (_req, res) => {
  try {
    if (mongoose.connection.readyState !== 1) {
      return res.status(503).json({ message: 'Database is not connected yet. Check backend terminal and MongoDB Atlas settings.' })
    }
    const bookings = await Booking.find().sort({ createdAt: -1 }).maxTimeMS(10000)
    res.json(bookings)
  } catch (error) {
    console.error('GET /api/bookings failed:', error.message)
    res.status(500).json({ message: 'Could not load bookings.', detail: error.message })
  }
})

app.post('/api/bookings', async (req, res) => {
  try {
    if (mongoose.connection.readyState !== 1) {
      return res.status(503).json({ message: 'Database is not connected.' })
    }

    const { guestName, roomName, roomPrice, checkIn, checkOut } = req.body
    if (!guestName || !roomName || roomPrice === undefined || !checkIn || !checkOut) {
      return res.status(400).json({ message: 'Please complete all booking fields.' })
    }
    if (new Date(checkOut) <= new Date(checkIn)) {
      return res.status(400).json({ message: 'Check-out must be after check-in.' })
    }

    const booking = await Booking.create({
      guestName,
      roomName,
      roomPrice: Number(roomPrice),
      checkIn,
      checkOut
    })
    res.status(201).json({ message: 'Booking saved successfully!', booking })
  } catch (error) {
    console.error('POST /api/bookings failed:', error.message)
    res.status(500).json({ message: 'Could not save booking.', detail: error.message })
  }
})

async function startServer() {
  try {
    if (!process.env.MONGO_URI || process.env.MONGO_URI.includes('YOUR-CLUSTER')) {
      throw new Error('MONGO_URI is missing. Copy .env.example to .env and add your MongoDB Atlas connection string.')
    }
    await mongoose.connect(process.env.MONGO_URI, {
      serverSelectionTimeoutMS: 10000,
      connectTimeoutMS: 10000
    })
    console.log('MongoDB connected successfully!')
  } catch (error) {
    console.error('MongoDB connection failed:', error.message)
    console.error('Check backend/.env, Atlas Network Access, and database username/password.')
  }

  const server = app.listen(PORT, '127.0.0.1', () => {
    console.log(`HotelPro server running at http://127.0.0.1:${PORT}`)
  })

  server.on('error', (error) => {
    if (error.code === 'EADDRINUSE') {
      console.error(`Port ${PORT} is already in use. Stop the other process or change PORT in backend/.env.`)
    } else {
      console.error('Server error:', error.message)
    }
  })
}

startServer()
