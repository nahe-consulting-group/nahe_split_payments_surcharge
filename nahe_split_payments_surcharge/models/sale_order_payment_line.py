from odoo import models, fields, api


class SaleOrderPaymentLine(models.Model):
    _name = "sale.order.payment.line"
    _description = "Payment Plan Lines"

    order_id = fields.Many2one("sale.order", string="Sale Order", ondelete="cascade")
    payment_amount = fields.Float(string="Amount to Pay")
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")

    pricelist_item_id = fields.Many2one(
        "product.pricelist.item",
        string="Pricelist Item",
        domain="[('pricelist_id', '=', pricelist_id)]",
    )

    original_amount_paid = fields.Float(
        string="Original Amount Paid",
        readonly=True,
        compute="_compute_original_amount_paid",
    )

    @api.onchange("pricelist_item_id")
    def _onchange_pricelist_item_id(self):
        if self.pricelist_item_id and self.pricelist_item_id.price_discount:
            remaining_original_amount = self.order_id.remaining_amount
            surcharge_percentage = abs(self.pricelist_item_id.price_discount)
            self.payment_amount = remaining_original_amount * (
                1 + surcharge_percentage / 100
            )

    @api.depends("payment_amount")
    def _compute_original_amount_paid(self):
        for record in self:
            surcharge_percentage = abs(record.pricelist_item_id.price_discount)
            record.original_amount_paid = record.payment_amount / (
                1 + surcharge_percentage / 100
            )
