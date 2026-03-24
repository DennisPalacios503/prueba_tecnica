{
    'name': 'Library Management',
    'version': '1.0.0',
    'category': 'Services',
    'summary': 'Módulo para gestión de biblioteca',
    'description': """
        Módulo principal del sistema de gestión de biblioteca.
    """,
    'author': 'Dennis Palacios',
    'website': '',
    'depends': [
        'base',
        'contacts',  # Para extender res.partner 
        'mail',      # Para avisos automáticos y mensajería
        'website',   # Para el Portal del Socio 
        'point_of_sale', # Integración POS
        ],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'data/library_sequence.xml', 
        'data/ir_cron.xml',   
        'data/library_data.xml',  
        'views/library_member_view.xml',
        'views/library_book_view.xml',        
        'views/library_loan_view.xml',        
        'views/library_portal_templates.xml',
    ],
    'installable': True,
    'application': True,   
    'auto_install': False,
    'license': 'LGPL-3',
}