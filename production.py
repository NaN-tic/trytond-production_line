# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta


class WorkCenterCategory(metaclass=PoolMeta):
    __name__ = 'production.work.center.category'

    is_line = fields.Boolean('Is Line')

