from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_surcharge_product = fields.Boolean("Is Surcharge Product", default=False)
