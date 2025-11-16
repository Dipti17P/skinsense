# Razorpay Integration Setup

## Steps to Configure Razorpay

### 1. Create Razorpay Account
1. Go to https://razorpay.com/
2. Sign up for a free account
3. Complete the verification process

### 2. Get API Keys
1. Login to Razorpay Dashboard: https://dashboard.razorpay.com/
2. Go to **Settings** → **API Keys**
3. Click on **Generate Test Key** (for development)
4. Copy your:
   - **Key ID** (starts with `rzp_test_`)
   - **Key Secret**

### 3. Update Django Settings
Open `skinsense/settings.py` and update:

```python
RAZORPAY_KEY_ID = 'rzp_test_YOUR_KEY_ID_HERE'
RAZORPAY_KEY_SECRET = 'YOUR_KEY_SECRET_HERE'
```

### 4. Test Payment
1. Run the server: `python manage.py runserver`
2. Add products to cart
3. Go to checkout
4. Click "Pay with Razorpay"
5. Use Razorpay test cards:
   - **Card Number**: 4111 1111 1111 1111
   - **CVV**: Any 3 digits
   - **Expiry**: Any future date

### 5. Go Live (Production)
When ready for production:
1. Complete KYC verification in Razorpay Dashboard
2. Generate **Live API Keys** (starts with `rzp_live_`)
3. Update settings.py with live keys
4. Test thoroughly before going live

## Features Implemented
✅ Razorpay checkout integration
✅ Payment verification with signature
✅ Order creation with Razorpay
✅ Secure payment processing
✅ Multiple payment methods (Cards, UPI, Net Banking, Wallets)
✅ Auto cart clearing after successful payment
✅ Payment success page with order ID

## Payment Methods Supported
- 💳 Credit/Debit Cards (Visa, Mastercard, RuPay)
- 📱 UPI (Google Pay, PhonePe, Paytm)
- 🏦 Net Banking (All major banks)
- 👛 Wallets (Paytm, PhonePe, Amazon Pay)
- 💰 EMI Options

## Important Notes
- Never commit API keys to version control
- Use environment variables for production
- Keep test and live keys separate
- Test thoroughly before going live
- Razorpay charges 2% + GST per transaction
