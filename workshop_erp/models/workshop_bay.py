# -*- coding: utf-8 -*-

from odoo import models, fields


class WorkshopBay(models.Model):
    """ Workshop Bay """
    _name = 'workshop.bay'
    _description = 'Bay'
    _inherit = ['mail.thread']

    name = fields.Char(required=True, translate=True)
    employee_id = fields.Many2one('hr.employee', string="Assigned Employee", tracking=True)
    status = fields.Selection(selection=[
        ('free', 'Free'),
        ('occupied', 'Occupied'),
        ('closed', 'Closed')], string='Status', tracking=True, default='free')
    type = fields.Selection(selection=[
        ('washing','Wash'),
        ('alignment','Alignment'),
        ('express','Express'),
        ('general','General'),
        ('paint','Painting')
    ], tracking=True, required=True)
    ongoing_job_id = fields.Many2one('workshop.job.order', string="Ongoing Job", readonly=True)

    def action_open(self):
        """workshop Bay Open"""
        self.status = 'free'

    def action_close(self):
        """workshop Bay Close"""
        self.status = 'closed'

