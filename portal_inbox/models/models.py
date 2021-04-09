# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Inbox(models.Model):
    _name = 'portal.inbox'

    name = fields.Char('Subject',readonly=True)
    student_id = fields.Many2one('op.student',string='Student',readonly=True)
    teacher_id = fields.Many2one('op.faculty',string='Teacher',readonly=True)
    message = fields.Text('Message',readonly=True)
    date = fields.Date('Date')

class Sent(models.Model):
    _name = 'portal.sent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Subject', track_visibility='onchange')
    student_id = fields.Many2many('op.student',string='Student', track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'),
                              ('sent', 'Sent')
                              ],default='draft', track_visibility='onchange')
    message = fields.Text('Message', track_visibility='onchange')
    read_by_student = fields.Boolean(default=False)
    sent_date = fields.Datetime(string='Date')

    def send(self):
        self.state = 'sent'
        self.sent_date = fields.Datetime.now()
