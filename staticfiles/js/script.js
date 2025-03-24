document.getElementById('paymentForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const amount = document.getElementById('amount').value * 100; // Convert to kobo

    const handler = PaystackPop.setup({
        key: 'YOUR_PUBLIC_KEY', // Replace this with your actual Paystack public key
        email: email,
        amount: amount,
        currency: 'NGN',
        callback: function(response) {
            alert('Payment successful! Reference: ' + response.reference);
        },
        onClose: function() {
            alert('Payment window closed.');
        }
    });

    handler.openIframe();
});
