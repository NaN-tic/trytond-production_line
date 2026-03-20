# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta


class ProductBom(metaclass=PoolMeta):
    __name__ = 'product.product-production.bom'

    line = fields.Many2One(
        'production.work.center', 'Line',
        domain=[
            ('category.is_line', '=', True),
            ],
        ondelete='RESTRICT')

    @fields.depends('routing')
    def on_change_routing(self):
        if self.routing and getattr(self.routing, 'line', None):
            self.line = self.routing.line


class ProductionLeadTime(metaclass=PoolMeta):
    __name__ = 'production.lead_time'

    line = fields.Many2One(
        'production.work.center', 'Line',
        domain=[
            ('category.is_line', '=', True),
            ],
        ondelete='RESTRICT')

    @fields.depends('routing')
    def on_change_routing(self):
        if self.routing and getattr(self.routing, 'line', None):
            self.line = self.routing.line

