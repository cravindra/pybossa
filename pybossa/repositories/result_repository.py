# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SciFabric LTD.
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy.exc import IntegrityError

from pybossa.model.result import Result
from pybossa.exc import WrongObjectError, DBIntegrityError


class ResultRepository(object):

    def __init__(self, db):
        self.db = db

    def get(self, id):
        return self.db.session.query(Result).get(id)

    def get_by(self, **attributes):
        return self.db.session.query(Result).filter_by(**attributes).first()

    def filter_by(self, limit=None, offset=0, **filters):
        query = self.db.session.query(Result).filter_by(**filters)
        query = query.order_by(Result.id).limit(limit).offset(offset)
        return query.all()

    def _validate_can_be(self, action, result):
        if not isinstance(result, Result):
            name = result.__class__.__name__
            msg = '%s cannot be %s by %s' % (name, action, self.__class__.__name__)
            raise WrongObjectError(msg)
