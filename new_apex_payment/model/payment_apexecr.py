from odoo import models, fields, api


class PaymentAcquirerApexECR(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('apexecr', 'ApexECR')],
        ondelete={'apexecr': 'set default'}
    )

    apexecr_merchant_id = fields.Char('Merchant ID', required_if_provider='apexecr')
    apexecr_terminal_id = fields.Char('Terminal ID', required_if_provider='apexecr')
    apexecr_secure_key = fields.Char('Secure Key', required_if_provider='apexecr')
    apexecr_wsdl_url = fields.Char('WSDL URL', default='https://apex-ecr-server/wsdl-url')

    def _get_apexecr_currency_code(self, currency):
        # Map Odoo currency to ApexECR numeric codes
        currency_codes = {
            'JOD': '400',
            'USD': '840',
            'EUR': '978'
        }
        return currency_codes.get(currency.name, '400')
