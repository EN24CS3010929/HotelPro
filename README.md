# HotelPro — Complete Starter Project

HotelPro is a simple hotel booking demo with:
- React + Vite frontend
- Express backend
- MongoDB Atlas database
- Booking form
- Admin dashboard at `/admin`

## 1. Requirements
Install Node.js (LTS) on your computer. You already have VS Code.

## 2. Set up the backend
1. Open this folder in VS Code.
2. Open a terminal and run:
   ```powershell
   cd backend
   npm install
   ```
3. Copy `.env.example` to a new file named `.env`.
4. Open `backend/.env` and replace the example `MONGO_URI` with your MongoDB Atlas connection string. Do not share this file publicly.
5. Start the backend:
   ```powershell
   npm run dev
   ```
6. Test in your browser:
   - http://127.0.0.1:5000/
   - http://127.0.0.1:5000/test
   - http://127.0.0.1:5000/api/bookings

Keep this terminal open.

## 3. Set up the frontend
Open a second terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open the URL Vite prints in the terminal (usually http://localhost:5173 or http://localhost:5174).

Keep this terminal open too.

## 4. Use the project
- On the home page, choose a room and submit a booking.
- Open `/admin` on the same frontend URL to view bookings. Example: http://localhost:5173/admin
- The backend API is at http://127.0.0.1:5000.

## Common fixes
- If the frontend says it cannot connect, check that the backend terminal is still running.
- If port 5000 is busy, stop the other server using that port, then restart this project.
- In MongoDB Atlas, add your current IP under Security / Network Access.
- Ensure the database user and password in `MONGO_URI` are correct. URL-encode special characters in the password.
- `.env` is intentionally not included because it contains your private database credentials.

This is a starter project, not a deployed public website. It has no admin login yet, so do not expose the admin page publicly.
