import os
import sqlite3
from datetime import date, datetime, timedelta
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="HotelPro — Luxury Hotel & Booking",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .hero-eyebrow {
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.8rem;
        color: #38bdf8;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 600;
        line-height: 1.2;
        margin-bottom: 0.8rem;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 650px;
    }
    
    .room-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .room-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .room-price {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0f172a;
    }
    
    .stat-badge {
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-pending {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-confirmed {
        background: #dcfce7;
        color: #166534;
    }
    
    .badge-cancelled {
        background: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

# Rooms Catalog
ROOMS = [
    {
        "id": 1,
        "name": "Standard Room",
        "price": 1500,
        "tag": "Comfort made simple",
        "description": "A welcoming space with the essentials for a restful stay.",
        "amenities": ["Wi-Fi", "Air Conditioning", "Queen Bed", "En-suite Bathroom"],
        "icon": "🛏️"
    },
    {
        "id": 2,
        "name": "Deluxe Room",
        "price": 2500,
        "tag": "A little more room",
        "description": "More space, extra comfort, and a calm, peaceful atmosphere.",
        "amenities": ["High-speed Wi-Fi", "Balcony View", "King Bed", "Smart TV", "Mini Fridge"],
        "icon": "🛋️"
    },
    {
        "id": 3,
        "name": "Luxury Suite",
        "price": 4000,
        "tag": "Your special escape",
        "description": "A spacious suite designed for a truly memorable luxury stay.",
        "amenities": ["Panoramic View", "Jacuzzi", "King Bed", "Living Area", "Complimentary Breakfast"],
        "icon": "👑"
    }
]

# Database Layer (MongoDB Atlas with SQLite Fallback)
def get_db():
    mongo_uri = None
    if "MONGO_URI" in st.secrets:
        mongo_uri = st.secrets["MONGO_URI"]
    elif os.environ.get("MONGO_URI"):
        mongo_uri = os.environ.get("MONGO_URI")
    
    if mongo_uri:
        try:
            from pymongo import MongoClient
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            db = client.get_default_database() or client['hotelpro']
            return "mongo", db
        except Exception:
            pass
            
    # SQLite fallback (guaranteed to work everywhere including Streamlit Cloud)
    conn = sqlite3.connect("hotelpro.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guestName TEXT NOT NULL,
            roomName TEXT NOT NULL,
            roomPrice REAL NOT NULL,
            checkIn TEXT NOT NULL,
            checkOut TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            createdAt TEXT NOT NULL
        )
    """)
    conn.commit()
    return "sqlite", conn

db_type, db_conn = get_db()

def fetch_bookings():
    if db_type == "mongo":
        try:
            records = list(db_conn.bookings.find().sort("createdAt", -1))
            for r in records:
                r["id"] = str(r.pop("_id"))
            return records
        except Exception:
            pass
            
    # SQLite
    cursor = db_conn.cursor()
    cursor.execute("SELECT id, guestName, roomName, roomPrice, checkIn, checkOut, status, createdAt FROM bookings ORDER BY id DESC")
    rows = cursor.fetchall()
    return [
        {
            "id": r[0],
            "guestName": r[1],
            "roomName": r[2],
            "roomPrice": r[3],
            "checkIn": r[4],
            "checkOut": r[5],
            "status": r[6],
            "createdAt": r[7]
        }
        for r in rows
    ]

def create_booking(guest_name, room_name, room_price, check_in, check_out):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if db_type == "mongo":
        try:
            db_conn.bookings.insert_one({
                "guestName": guest_name,
                "roomName": room_name,
                "roomPrice": room_price,
                "checkIn": str(check_in),
                "checkOut": str(check_out),
                "status": "Pending",
                "createdAt": created_at
            })
            return True
        except Exception:
            pass
            
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (guestName, roomName, roomPrice, checkIn, checkOut, status, createdAt)
        VALUES (?, ?, ?, ?, ?, 'Pending', ?)
    """, (guest_name, room_name, room_price, str(check_in), str(check_out), created_at))
    db_conn.commit()
    return True

def update_booking_status(booking_id, new_status):
    if db_type == "mongo":
        try:
            from bson import ObjectId
            db_conn.bookings.update_one({"_id": ObjectId(booking_id)}, {"$set": {"status": new_status}})
            return True
        except Exception:
            pass
            
    cursor = db_conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (new_status, booking_id))
    db_conn.commit()
    return True

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🏨 **HotelPro**")
    st.caption("Your Stay, Made Special")
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Home & Rooms", "📅 Book a Stay", "📊 Admin Dashboard"], index=0)
    
    st.markdown("---")
    st.markdown(f"**Database Engine:** `{'MongoDB Atlas' if db_type == 'mongo' else 'SQLite (Embedded)'}`")
    st.caption("All bookings are persisted safely in real time.")
    st.markdown("---")
    st.caption("Developed by **EN24CS3010929**")

# PAGE 1: HOME & ROOMS
if page == "🏠 Home & Rooms":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-eyebrow">✨ YOUR STAY, MADE SPECIAL</div>
        <div class="hero-title">Find your place to feel at home.</div>
        <div class="hero-subtitle">
            Thoughtful rooms, warm hospitality, and a smoother way to plan your next stay.
            Browse our catalog below and reserve your experience today.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Available Rooms & Suites")
    cols = st.columns(3)
    
    for i, room in enumerate(ROOMS):
        with cols[i]:
            st.markdown(f"""
            <div class="room-card">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">{room['icon']}</div>
                <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 700;">{room['tag']}</div>
                <h3 style="margin: 0.2rem 0; color: #0f172a;">{room['name']}</h3>
                <p style="color: #64748b; font-size: 0.9rem; min-height: 48px;">{room['description']}</p>
                <div style="margin: 1rem 0;">
                    <span class="room-price">₹{room['price']:,}</span>
                    <span style="color: #64748b; font-size: 0.85rem;"> / night</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("✨ Included Amenities"):
                for amenity in room["amenities"]:
                    st.write(f"• {amenity}")
            
            if st.button(f"Book {room['name']}", key=f"btn_room_{room['id']}", use_container_width=True):
                st.session_state["selected_room_id"] = room["id"]
                st.session_state["nav_to_book"] = True
                st.rerun()

# PAGE 2: BOOK A STAY
elif page == "📅 Book a Stay":
    st.markdown("## 📅 Reserve Your Stay")
    st.write("Complete the details below to submit your booking request.")
    st.markdown("---")
    
    default_room_idx = 0
    if "selected_room_id" in st.session_state:
        for idx, r in enumerate(ROOMS):
            if r["id"] == st.session_state["selected_room_id"]:
                default_room_idx = idx
                break
                
    col1, col2 = st.columns([1.4, 1])
    
    with col1:
        with st.form("booking_form", clear_on_submit=False):
            guest_name = st.text_input("Full Name", placeholder="e.g. John Doe")
            
            selected_room = st.selectbox(
                "Choose Room",
                options=ROOMS,
                index=default_room_idx,
                format_func=lambda r: f"{r['name']} — ₹{r['price']:,} / night"
            )
            
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                check_in = st.date_input("Check-in Date", min_value=date.today())
            with col_date2:
                check_out = st.date_input("Check-out Date", min_value=date.today() + timedelta(days=1))
                
            special_requests = st.text_area("Special Requests (Optional)", placeholder="Late check-in, dietary preferences, etc.")
            
            submitted = st.form_submit_button("Confirm Booking Request", use_container_width=True)
            
            if submitted:
                if not guest_name.strip():
                    st.error("Please enter your name.")
                elif check_out <= check_in:
                    st.error("Check-out date must be after check-in date.")
                else:
                    success = create_booking(
                        guest_name=guest_name.strip(),
                        room_name=selected_room["name"],
                        room_price=selected_room["price"],
                        check_in=check_in,
                        check_out=check_out
                    )
                    if success:
                        st.balloons()
                        st.success(f"🎉 Booking request saved for **{guest_name}**! Status is **Pending**.")
    
    with col2:
        st.markdown("### 📋 Booking Summary")
        nights = max(1, (check_out - check_in).days) if 'check_out' in locals() and 'check_in' in locals() else 1
        room_obj = selected_room if 'selected_room' in locals() else ROOMS[0]
        total_estimate = nights * room_obj["price"]
        
        st.info(f"""
        - **Room**: {room_obj['name']}
        - **Rate**: ₹{room_obj['price']:,} per night
        - **Duration**: {nights} night(s)
        - **Estimated Total**: **₹{total_estimate:,}**
        """)
        st.caption("ℹ️ Requests are processed with 'Pending' status and reviewed in the Admin Dashboard.")

# PAGE 3: ADMIN DASHBOARD
elif page == "📊 Admin Dashboard":
    st.markdown("## 📊 HotelPro Management Dashboard")
    st.write("Track and manage real-time guest reservations.")
    
    bookings = fetch_bookings()
    
    total = len(bookings)
    pending = sum(1 for b in bookings if b.get("status") == "Pending")
    confirmed = sum(1 for b in bookings if b.get("status") == "Confirmed")
    cancelled = sum(1 for b in bookings if b.get("status") == "Cancelled")
    revenue = sum(float(b.get("roomPrice", 0)) for b in bookings if b.get("status") == "Confirmed")
    
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Bookings", total)
    m2.metric("Pending Requests", pending)
    m3.metric("Confirmed Stays", confirmed)
    m4.metric("Confirmed Revenue", f"₹{int(revenue):,}")
    st.markdown("---")
    
    if not bookings:
        st.info("No bookings found yet. Go to the 'Book a Stay' tab to create a test reservation!")
    else:
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Confirmed", "Cancelled"], index=0)
        filtered = [b for b in bookings if status_filter == "All" or b.get("status") == status_filter]
        
        # Display Table
        df = pd.DataFrame([
            {
                "ID": b["id"],
                "Guest": b["guestName"],
                "Room": b["roomName"],
                "Price/Night": f"₹{int(b['roomPrice']):,}",
                "Check-In": b["checkIn"],
                "Check-Out": b["checkOut"],
                "Status": b["status"],
                "Date Booked": b["createdAt"]
            }
            for b in filtered
        ])
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### ⚡ Quick Status Actions")
        pending_list = [b for b in bookings if b.get("status") == "Pending"]
        
        if pending_list:
            action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
            with action_col1:
                selected_b_id = st.selectbox(
                    "Select Pending Booking",
                    options=[b["id"] for b in pending_list],
                    format_func=lambda x: next(f"ID {b['id']} - {b['guestName']} ({b['roomName']})" for b in pending_list if b["id"] == x)
                )
            with action_col2:
                st.write("")
                st.write("")
                if st.button("✅ Confirm Booking", use_container_width=True):
                    update_booking_status(selected_b_id, "Confirmed")
                    st.success("Booking confirmed!")
                    st.rerun()
            with action_col3:
                st.write("")
                st.write("")
                if st.button("❌ Cancel Booking", use_container_width=True):
                    update_booking_status(selected_b_id, "Cancelled")
                    st.warning("Booking cancelled.")
                    st.rerun()
        else:
            st.caption("No pending requests to approve at this time.")
