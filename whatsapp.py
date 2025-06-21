import os
from datetime import datetime, timedelta
import re
import time
import pywhatkit

def format_phone_number(phone_number):
    """
    Format phone number to include country code (e.g., +91XXXXXXXXXX)
    """
    # Remove any non-digit characters
    phone_number = re.sub(r'\D', '', phone_number)
    
    # Add country code if not present
    if not phone_number.startswith('91'):
        phone_number = '91' + phone_number
    
    # Add plus sign for pywhatkit
    return '+' + phone_number

def send_booking_confirmation(phone_number, booking_details):
    """
    Send booking confirmation via WhatsApp using pywhatkit
    """
    try:
        # Format phone number
        formatted_number = format_phone_number(phone_number)
        
        # Format the message
        message = f"""
🎫 *Booking Confirmation*

Dear {booking_details['name']},

Your booking has been confirmed! Here are the details:

*Monument:* {booking_details['monument_name']}
*Visit Date:* {booking_details['visit_date'].strftime('%d %B %Y')}
*Number of Visitors:* {booking_details['visitors']}
*Total Amount:* ₹{booking_details['total_amount']}
*Booking ID:* {booking_details['id']}

Please present this booking confirmation at the entrance.

Thank you for choosing ITIHASA!"""

        # Configure pywhatkit for instant sending with minimal wait time
        pywhatkit.sendwhatmsg_instantly(
            phone_no=formatted_number,
            message=message,
            wait_time=5,  # Increased wait time to 5 seconds
            tab_close=True,
            close_time=1
        )
        
        return True, "Message sent successfully"
            
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        return False, str(e) 