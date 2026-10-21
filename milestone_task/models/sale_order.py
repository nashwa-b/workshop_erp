# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    """Extends sales model to create project, tasks and subtasks"""
    _inherit = 'sale.order'

    def action_create_project_sale(self):
        """Create Project with the SO name and tasks with the order line"""
        Project = self.env['project.project']
        Task = self.env['project.task']

        if not self.project_id:
            project = Project.create({
                'name': self.name,
                'partner_id': self.partner_id.id,
            })
            self.project_id = project.id

            print(project.name)

        milestones = {}
        for line in self.order_line:

            milestone = line.milestone

            if milestone not in milestones:
                milestones[milestone] = Task.create({
                    'name': f"Milestone {milestone}",
                    'project_id': self.project_id.id,
                })
            print("tt", milestones[milestone])

            task = milestones[milestone]

            Task.create({
                'name': f"Milestone {milestone} - {line.product_id.name}",
                'project_id': self.project_id.id,
                'parent_id': task.id,
            })

    def action_update_project(self):
        """Update tasks according to changes in order lines"""
        
        tasks = self.env['project.task'].search([('project_id', '=', self.project_id.id)])
        tasks.unlink()

        return self.action_create_project_sale()
