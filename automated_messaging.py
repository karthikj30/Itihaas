import schedule
import time
from datetime import datetime
from .whatsapp import send_booking_confirmation
from .models import Booking, db
from website import create_app

def send_pending_messages():
    """
    Check for pending bookings and send WhatsApp messages
    """
    app = create_app()
    with app.app_context():
        try:
            # Get all confirmed bookings that haven't received a message
            pending_bookings = Booking.query.filter_by(
                status='Confirmed',
                whatsapp_sent=False
            ).all()  # Get all pending bookings
            
            if not pending_bookings:
                return  # Skip if no pending bookings
            
            print(f"Found {len(pending_bookings)} pending messages to send")
            
            for booking in pending_bookings:
                try:
                    booking_details = {
                        'id': booking.id,
                        'name': booking.name,
                        'monument_name': booking.monument_name,
                        'visit_date': booking.visit_date,
                        'visitors': booking.visitors,
                        'total_amount': booking.total_amount
                    }
                    
                    # Send WhatsApp message
                    success, message = send_booking_confirmation(booking.phone, booking_details)
                    
                    if success:
                        # Mark booking as message sent
                        booking.whatsapp_sent = True
                        db.session.commit()
                        print(f"Message sent successfully to {booking.name} for booking {booking.id}")
                    else:
                        print(f"Failed to send message to {booking.name} for booking {booking.id}: {message}")
                    
                except Exception as e:
                    print(f"Error processing booking {booking.id}: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in automated messaging: {str(e)}")

def start_scheduler():
    """
    Start the scheduler for automated messaging
    """
    # Schedule the task to run every 30 seconds
    schedule.every(30).seconds.do(send_pending_messages)
    
    print("WhatsApp message scheduler started")
    print("Checking for pending messages every 30 seconds...")
    print("Make sure WhatsApp Web is logged in in your default browser")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"Error in scheduler: {str(e)}")
            time.sleep(5)  # Wait a bit before retrying 