# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta


class WorkCenterCategory(metaclass=PoolMeta):
    __name__ = 'production.work.center.category'

    is_line = fields.Boolean('Is Line')


class Production(metaclass=PoolMeta):
    __name__ = 'production'

    line = fields.Many2One(
        'production.work.center', 'Line',
        domain=[
            ('category.is_line', '=', True),
            ],
        ondelete='RESTRICT')

    @fields.depends('product', 'bom', 'routing', 'line', 'work_center',
        methods=['explode_bom', 'set_planned_start_date',
            '_set_defaults_from_product_bom'])
    def on_change_product(self):
        super().on_change_product()
        self._set_defaults_from_product_bom()
        self.explode_bom()
        self.set_planned_start_date()

    @fields.depends('product', 'bom', 'routing', 'line', 'work_center',
        methods=['explode_bom', 'set_planned_start_date',
            '_set_defaults_from_product_bom'])
    def on_change_bom(self):
        super().on_change_bom()
        self._set_defaults_from_product_bom()
        self.explode_bom()
        self.set_planned_start_date()

    @fields.depends('product', 'bom', 'routing', 'line', 'work_center')
    def _set_defaults_from_product_bom(self):
        line = self._get_product_bom_line()
        if not line:
            if not self.product:
                self.bom = None
                self.routing = None
                self.line = None
                self.work_center = None
            return
        self.bom = line.bom
        self.routing = line.routing
        self.line = line.line
        self.work_center = line.line

    def _get_product_bom_line(self):
        if not self.product:
            return
        if self.bom:
            exact = []
            fallback = []
            for line in self.product.boms:
                if line.bom != self.bom:
                    continue
                if self.routing and line.routing == self.routing:
                    exact.append(line)
                elif not self.routing:
                    exact.append(line)
                else:
                    fallback.append(line)
            if exact:
                return exact[0]
            if fallback:
                return fallback[0]
        if self.product.boms:
            return min(
                self.product.boms,
                key=lambda line: (
                    line.sequence if line.sequence is not None else float('inf'),
                    line.id or 0))
