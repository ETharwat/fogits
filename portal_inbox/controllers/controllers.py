# -*- coding: utf-8 -*-
from odoo import http, _, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class MessagesPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(MessagesPortal, self)._prepare_portal_layout_values()
        current_user = request.env.user.id
        current_student = request.env['op.student'].sudo().search([('user_id', '=', current_user)])
        inbox = request.env['portal.sent'].sudo().search(
            [('student_id', 'in', current_student.id), ('state', '=', 'sent'),('read_by_student', '!=', True)])

        values['message_count'] = len(inbox)

        return values

class PortalInbox(http.Controller):
    @http.route(['/my/incoming'], type='http', auth="user", website=True)
    def portal_incoming(self, **kw):
        current_user = request.env.user.id
        current_student = request.env['op.student'].sudo().search([('user_id', '=', current_user)])
        inbox = request.env['portal.sent'].sudo().search([('student_id', 'in', current_student.id),
                                                          ('state', '=', 'sent')])
        values = {
            'student': current_student,
            'inbox': inbox,
        }
        return request.render("portal_inbox.portal_incoming_messages", values)

    @http.route(['/my/incoming/<int:message_id>'], type='http', auth="public", website=True)
    def portal_my_incoming(self, message_id, **kw):
        current_student_assignment = request.env['portal.sent'].sudo().search([('id', '=', message_id)])
        values = {
            'message': current_student_assignment
        }
        request.env['portal.sent'].sudo().search([('id', '=', message_id)]).write({'read_by_student':True})
        return request.render("portal_inbox.portal_incoming_details", values)


class PortalOutgoing(http.Controller):
    @http.route(['/my/outgoing'], type='http', auth="user", website=True)
    def portal_outgoing(self, **kw):
        current_user = request.env.user.id
        current_student = request.env['op.student'].sudo().search([('user_id', '=', current_user)])
        inbox = request.env['portal.inbox'].sudo().search([('student_id', '=', current_student.id)])
        teachers = request.env['op.faculty'].sudo().search([])
        values = {
            'inbox': inbox,
            'teachers':teachers,
        }
        return request.render("portal_inbox.portal_outgoing_messages", values)

    @http.route(['/my/outgoing/<int:message_id>'], type='http', auth="public", website=True)
    def portal_my_outgoing(self, message_id, access_token=None, report_type=None, download=False, **kw):
        current_message = request.env['portal.inbox'].sudo().sudo().search([('id', '=', message_id)])
        values = {
            'message': current_message
        }
        return request.render("portal_inbox.portal_outgoing_details", values)

    @http.route(['/NewMessage'], type='http', auth="user", website=True)
    def portal_new_outgoing(self, **kw):
        current_user = request.env.user.id
        current_student = request.env['op.student'].sudo().search([('user_id', '=', current_user)])
        teachers = request.env['op.faculty'].sudo().search([])
        values = {
            'student': current_student,
            'teachers':teachers,
        }
        return request.render("portal_inbox.portal_new_outgoing_messages", values)

    @http.route(['/MessageSent'], type='http', auth="user", methods=['POST'], website=True)
    def portal_sent_outgoing(self, **kw):
        current_user = request.env.user.id
        current_student = request.env['op.student'].sudo().search([('user_id', '=', current_user)])
        request.env['portal.inbox'].sudo().create({'name':kw['subject'],
                                                   'student_id':current_student.id,
                                                   'teacher_id':kw['teachers'],
                                                   'message':kw['message']})

        return request.redirect('/my/outgoing')
