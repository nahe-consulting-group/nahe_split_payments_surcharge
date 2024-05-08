# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Split Payments with surcharges",
    "summary": """
    'Manages payment plans for sales orders, allowing the application of differentiated rates and automatic surcharge calculations.'""",
    "author": "Nahe Consulting Group",
    "maintainers": ["nahe-consulting-group"],
    "description": """This module allows users to create and manage custom payment plans for sales orders. Features include:
        - Creation of payment plans linked to sales orders.
        - Addition of payment lines with specific rates including automatic surcharges based on pricelist forumla discounts.
        - Automatic calculation of payment amounts and tracking of remaining amounts to be paid.
        - Possibility to expand and adjust rates and calculations as future needs arise.""",
    "website": "https://nahe.com.ar/",
    "license": "AGPL-3",
    "category": "Sales",
    "version": "15.0.3.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["sale", "product", "base"],
    "data": [
        "views/sale_order.xml",
        "views/product_template.xml",
        "views/sale_order_payment_line_view.xml",
        "security/sale_payment_line_access.xml",
    ],
}
