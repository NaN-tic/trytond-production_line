# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import Pool

from . import product, production


def register():
    Pool.register(
        production.WorkCenterCategory,
        production.Production,
        product.ProductBom,
        product.ProductionLeadTime,
        module='production_line', type_='model')
