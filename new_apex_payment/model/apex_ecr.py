import logging
from odoo import models, fields, api, _
from zeep import Client
from zeep.transports import Transport
from requests import Session

_logger = logging.getLogger(__name__)

class ApexECRConfig(models.Model):
    _name = 'apex.ecr.config'
    _description = 'Apex ECR Configuration'

    name = fields.Char('Configuration Name', required=True)
    wsdl_url = fields.Char('ApexECR WSDL URL', required=True)
    tid = fields.Char('Terminal ID', required=True)
    mid = fields.Char('Merchant ID', required=True)
    secure_key = fields.Char('Merchant Secure Key', required=True)
    currency_code = fields.Char('Currency Code', required=True, default='400')
    tiller_username = fields.Char('Tiller Username')
    tiller_fullname = fields.Char('Tiller Full Name')
    soap_action = fields.Char('SOAP Action', required=True, default='http://tempuri.org/IEcrComInterface/Sale')
    endpoint_url = fields.Char('Endpoint URL', required=True, default='https://apex.switch.com.iq/Apex.SmartPos.EcrWebService/EcrComInterface.svc')
    api_key = fields.Char('API Key', help='API Key for additional authentication if required')
    client_id = fields.Char('Client ID', help='Client ID for OAuth or other authentication methods')
    client_secret = fields.Char('Client Secret', help='Client Secret for OAuth or other authentication methods')

class ApexECRTransaction(models.Model):
    _name = 'apex.ecr.transaction'
    _description = 'Apex ECR Transaction'

    config_id = fields.Many2one('apex.ecr.config', required=True)
    amount = fields.Float('Amount', required=True)
    invoice_number = fields.Char('Invoice Number', required=True)
    reference_number = fields.Char('Reference Number')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('success', 'Success'),
        ('error', 'Error')
    ], default='draft')
    response_message = fields.Text('Response Message')

    def send_to_apex(self):
        for rec in self:
            config = rec.config_id
            # Prepare SOAP client
            session = Session()
            session.verify = False  # Set to True if you have SSL certificates
            client = Client(wsdl=config.wsdl_url, transport=Transport(session=session))

            # Prepare request
            request_data = {
                'Config': {
                    'Tid': config.tid,
                    'Mid': config.mid,
                    'MerchantSecureKey': config.secure_key,
                    'EcrCurrencyCode': config.currency_code,
                    'EcrTillerUserName': config.tiller_username,
                    'EcrTillerFullName': config.tiller_fullname,
                },
                'Printer': {
                    'PrinterWidth': 40,
                    'EnablePrintPosReceipt': False,
                    'EnablePrintReceiptNote': 0,
                    'ReceiptNote': '',
                    'InvoiceNumber': rec.invoice_number,
                    'ReferenceNumber': rec.reference_number,
                },
                'TransactionType': 'SALE',
                'EcrAmount': rec.amount,
                'InvoiceNumber': rec.invoice_number,
            }

            try:
                # Set SOAPAction header
                client.transport.session.headers.update({
                    'SOAPAction': config.soap_action
                })

                # Send request to endpoint URL
                response = client.service.PerformFinancialTransaction(**request_data)
                # Parse response
                if response.WebResponseStatus == 'Success' and \
                   response.FinancialTxnResponseDE.PosRespCode == '00':
                    rec.status = 'success'
                    rec.response_message = response.FinancialTxnResponseDE.PosReceipt
                else:
                    rec.status = 'error'
                    rec.response_message = response.WebResponseErrorDesc or 'Unknown error'
            except Exception as e:
                rec.status = 'error'
                rec.response_message = str(e)
                _logger.error("ApexECR SOAP Error: %s", e)
