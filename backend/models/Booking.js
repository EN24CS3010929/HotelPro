const mongoose = require('mongoose')

const bookingSchema = new mongoose.Schema(
  {
    guestName: { type: String, required: true, trim: true },
    roomName: { type: String, required: true, trim: true },
    roomPrice: { type: Number, required: true, min: 0 },
    checkIn: { type: Date, required: true },
    checkOut: { type: Date, required: true },
    status: {
      type: String,
      enum: ['Pending', 'Confirmed', 'Cancelled'],
      default: 'Pending'
    }
  },
  { timestamps: true }
)

module.exports = mongoose.model('Booking', bookingSchema)
