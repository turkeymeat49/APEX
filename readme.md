"""
Prompt for GitHub Copilot:

I am integrating an Apex payment terminal with Odoo POS (version 16+) using a local Python SOAP bridge server at http://localhost:5000/pay.

I want to create a **single custom Odoo POS module** that:

1. Adds a new POS payment method called "ApexTerminal" with a boolean field `use_apex_terminal` to enable it.
2. Extends the POS frontend JS to:
   - Show a "Pay with Apex" button on the payment screen when ApexTerminal is selected.
   - On button click, send an HTTP POST request to `http://localhost:5000/pay` with JSON payload containing payment amount and currency.
   - Wait for the JSON response from the local server, which returns `{ "status": "approved" }` or `{ "status": "declined" }`.
   - If approved, automatically finalize and validate the POS order.
   - If declined, show an error message and allow retry.
3. Follow the structure and patterns from the OCA pos_payment_terminal module (https://github.com/OCA/pos/tree/14.0/pos_payment_terminal), adapted for Odoo 16+ OWL frontend.
4. Use modern Odoo POS OWL components, hooks (`useState`, `useListener`), and payment methods registration.
5. Provide minimal but complete example code snippets for:
   - Python model extension (`pos_payment_method`).
   - XML to add the field to payment method form.
   - JS module extending `PaymentScreen` or payment method widget.
   - HTTP communication with local server.
   - Order finalization on payment approval.

Please generate a single-file example combining these elements (Python, XML, JS) with comments explaining each part, so I can copy-paste and adapt it to my custom module.
"""
