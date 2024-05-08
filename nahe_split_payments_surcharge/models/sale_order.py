from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    original_total = fields.Monetary(
        string="Original Total", compute="_compute_original_total", store=True
    )
    remaining_amount = fields.Monetary(
        string="Remaining Amount", compute="_compute_remaining_amount", store=True
    )
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")
    payment_line_ids = fields.One2many(
        "sale.order.payment.line", "order_id", string="Payment Lines"
    )
    new_total_price = fields.Monetary(
        string="New Total",
        compute="_compute_new_total_price",
    )

    surcharge_done = fields.Boolean(
        string="Surcharge already aplyed", default=False, readonly=True
    )

    def add_surcharge_product(self):
        self.ensure_one()  # Asegura que la función se llama sobre un solo registro
        if self.surcharge_done:
            return  # No hagas nada si el recargo ya fue aplicado

        # Buscar el producto para el recargo financiero
        surcharge_product = self.env["product.template"].search(
            [("is_surcharge_product", "=", True)], limit=1
        )

        if not surcharge_product:
            return  # Si no se encuentra ningún producto, no se hace nada

        # Calcular el monto del recargo
        surcharge_amount = self.new_total_price - self.original_total
        if surcharge_amount <= 0:
            return  # Si no hay recargo que aplicar, no hacemos nada

        # Crear la línea del pedido de venta
        self.env["sale.order.line"].create(
            {
                "order_id": self.id,
                "product_id": surcharge_product.product_variant_id.id,
                "name": surcharge_product.name,
                "product_uom_qty": 1,
                "price_unit": surcharge_amount,
            }
        )

        # Marcar que el recargo fue aplicado
        self.surcharge_done = True

        # Recalcular los totales del pedido
        self._amount_all()

    @api.depends("order_line.price_total")
    def _compute_original_total(self):
        for order in self:
            if order.surcharge_done:
                return  # No hagas nada si el recargo ya fue aplicado
            order.original_total = order.amount_total

    @api.depends("payment_line_ids.original_amount_paid")
    def _compute_remaining_amount(self):
        for order in self:
            total_paid = sum(
                line.original_amount_paid for line in order.payment_line_ids
            )
            order.remaining_amount = order.original_total - total_paid

    @api.depends("payment_line_ids")
    def _compute_new_total_price(self):
        for order in self:
            total_client_paid = sum(
                line.payment_amount for line in order.payment_line_ids
            )
            order.new_total_price = total_client_paid + order.remaining_amount
