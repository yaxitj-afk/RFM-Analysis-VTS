# -*- coding: utf-8 -*-pack
{  # App information
    'name': 'RFM Analysis for Targeted Marketing Strategy',
    'category': 'Website',
    'version': '19.0.1.0',
    'summary': """The Odoo RFM Customer Segmentation module enables data-driven customer analysis using the RFM (Recency, Frequency, Monetary) model to identify high-value and at-risk customers. By evaluating last purchase date, total order count, and total revenue contribution, the module automatically segments customers into actionable groups for targeted email and marketing campaigns. This helps businesses personalize communication, improve engagement, increase conversion rates, and maximize customer lifetime value. With clear RFM-based segmentation inside Odoo, companies can make smarter marketing decisions and drive sustainable eCommerce sales growth.
                  Odoo RFM Analysis | Odoo Customer Segmentation | Odoo Marketing Automation | RFM Analysis in Odoo | Odoo Customer Lifetime Value |
                  Odoo Recency Frequency Monetary | Odoo eCommerce Analytics| Odoo Targeted Email Campaign | Odoo Customer Behavior Analysis |
                  Odoo Sales Intelligence Module | Odoo CRM Segmentation Tool | Odoo Marketing Strategy Module | Odoo Customer Value Analysis |
                  Odoo Data-Driven Marketing | Odoo Customer Retention Tool
vraja_featured_apps
                  """,
    'description': """""",
    # Dependencies
    'depends': ['sale_management', 'contacts','crm', 'web'],
    # Views
    'data': [
        "security/ir.model.access.csv",

        # Partner views
        'views/res_partner.xml',

        # Actions & views (must come before menus)
        "views/rfm_rule_views.xml",
        "views/rfm_segment_rule_views.xml",
        "views/rfm_segment_dashboard.xml",
        "views/res_company.xml",

        # Menus (after actions are defined)
        "views/rfm_menus.xml",

        # Data
        "data/rfm_rule_data.xml",
        'data/rfm_segment_data.xml',
        "data/rfm_segment_rule_data.xml",
        "data/partner_rfm_server_actions.xml",
        "data/rfm_cron.xml",
        # "data/rfm_segment_dashboard_data.xml"
    ],

    'images': ['static/description/cover.png'],
    'assets': {
        'web.assets_backend': [
            'rfm_analysis_vts/static/src/js/company_switch.js',
        ],
    },
    'author': 'Vraja Technologies',
    'maintainer': 'Vraja Technologies',
    'website': 'www.vrajatechnologies.com',
    'live_test_url': 'http://www.vrajatechnologies.com/contactus',
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '99',
    'currency': 'EUR',
    'license': 'OPL-1',
}
