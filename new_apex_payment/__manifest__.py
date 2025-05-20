{
    'name': 'Apex ECR Integration',
    'version': '1.0',
    'summary': 'Integrate Odoo with ApexECR payment terminals via SOAP',
    'author': 'Your Name',
    'category': 'Accounting/Payment',
    'depends': ['base', 'point_of_sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/apex_ecr_views.xml',
        'views/payment_acquirer_apexecr.xml',
        'data/ir_sequence.xml',
        # Add your views and security files here later
    ],
    'installable': True,
    'application': True,
}
