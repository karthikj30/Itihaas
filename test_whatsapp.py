from website.whatsapp import send_booking_confirmation
from datetime import datetime

def test_whatsapp():
    print("\n=== WhatsApp Message Test ===")
    print("Enter your phone number (without country code)")
    print("Example: 8850945234")
    print("=" * 30)
    
    while True:
        phone_number = input("\nEnter your phone number: ").strip()
        
        # Validate phone number
        if not phone_number.isdigit() or len(phone_number) != 10:
            print("Error: Please enter a valid 10-digit phone number")
            continue
            
        # Test booking details
        booking_details = {
            'id': 'TEST123',
            'name': 'Test User',
            'monument_name': 'Taj Mahal',
            'visit_date': datetime.now(),
            'visitors': 2,
            'total_amount': 1000
        }
        
        # Send test message
        print("\nSending test message...")
        success, message = send_booking_confirmation(phone_number, booking_details)
        
        if success:
            print("\n✅ Message scheduled successfully!")
            print("Please check your WhatsApp in about 30-60 seconds.")
            print("Make sure WhatsApp Web is set up on your computer.")
        else:
            print(f"\n❌ Error: {message}")
        
        # Ask if user wants to test another number
        again = input("\nDo you want to test another number? (y/n): ").lower()
        if again != 'y':
            break
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_whatsapp() 