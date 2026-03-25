# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json


class LibraryApi(http.Controller):

    @http.route(
        '/library/book/check_availability',
        type='http', auth='public', methods=['GET'], csrf=False
    )
    def check_book_availability(self, isbn=None, **kwargs):
        if not isbn:
            return Response(
                json.dumps({'error': 'Falta el parámetro ISBN'}),
                status=400, content_type='application/json'
            )

        book = request.env['library.book'].sudo().search(
            [('isbn', '=', isbn)], limit=1
        )

        if not book:
            return Response(
                json.dumps({'error': 'Libro no encontrado'}),
                status=404, content_type='application/json'
            )

        data = {
            'id': book.id,
            'title': book.name,
            'isbn': book.isbn,
            'is_available': book.is_available,
            'status': 'Disponible' if book.is_available else 'No disponible',
        }

        return Response(
            json.dumps(data),
            status=200, content_type='application/json'
        )