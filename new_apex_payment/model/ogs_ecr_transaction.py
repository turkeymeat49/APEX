from odoo import models, fields, api

class OGSECRTransaction(models.Model):
    _name = 'ogs.ecr.transaction'
    _description = 'OGS ECR Transaction'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('ogs.ecr.transaction'))
    transaction_type = fields.Selection([
        ('start', 'Start Session'),
        ('sale', 'Sale'),
        ('refund', 'Refund'),
        ('void', 'Void'),
        ('settle', 'Settlement'),
        ('last_txn_status', 'Last Transaction Status'),
    ], required=True)

    terminal_id = fields.Char(string='Terminal ID', required=True)
    merchant_id = fields.Char(string='Merchant ID')
    username = fields.Char(string='Tiller Username')
    fullname = fields.Char(string='Tiller Full Name')
    datetime = fields.Datetime(string='Transaction Datetime', required=True)
    currency_code = fields.Char(string='Currency Code', default='400')
    amount = fields.Monetary(string='Transaction Amount')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.JOD'))

    ecr_ref = fields.Char(string='ECR Reference')
    pos_ref = fields.Char(string='POS Reference')
    rrn = fields.Char(string='Retrieval Reference Number')
    auth_code = fields.Char(string='Authorization Code')
    batch_number = fields.Char(string='Batch Number')
    invoice_number = fields.Char(string='Invoice Number')
    is_approved = fields.Boolean(string='Is Approved')
    is_voided = fields.Boolean(string='Is Voided')
    is_reversal = fields.Boolean(string='Is Reversal')
    is_offline = fields.Boolean(string='Is Offline')
    response_code = fields.Char(string='Response Code')
    response_description = fields.Text(string='Response Description')

    pan = fields.Char(string='Masked PAN')
    issuer_name = fields.Char(string='Issuer Name')
    card_type = fields.Selection([
        ('L', 'Local'),
        ('F', 'Foreign'),
        ('other', 'Other')
    ], string='Card Type')
    card_slot = fields.Selection([
        (1, 'Manual Entry'),
        (2, 'Swipe'),
        (3, 'Chip Insert'),
        (4, 'Contactless')
    ], string='Card Slot')
    cvm_type = fields.Selection([
        ('00', 'No CVM'),
        ('01', 'Online PIN'),
        ('02', 'Offline PIN'),
        ('04', 'Signature'),
        ('80', 'PIN Bypass')
    ], string='CVM Type')

    # For future: you can create relational models for dcc and emv if needed
    # dcc_data = fields.Text(string='DCC Data (JSON)')
    # emv_data = fields.Text(string='EMV Data (JSON)')

    extra = fields.Text(string='Extra Data')
