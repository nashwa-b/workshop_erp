# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    """Extends sales model to create project, tasks and subtasks"""
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project')

    # is_clicked = fields.Boolean(default=False)

    def action_create_project_sale(self):
        """Create Project with the SO name and tasks with the order line"""
        # for order in self:
        Project = self.env['project.project']
        Task = self.env['project.task']

        project = Project.create({
            'name': self.name,
            'partner_id': self.partner_id.id,
            # 'project_id': order.id,
        })

        self.project_id = project.id

        print(project.name)

        milestones = {}
        for line in self.order_line:

            milestone = line.milestone

            if milestone not in milestones:
                milestones[milestone] = Task.create({
                    'name': f"Milestone {milestone}",
                    'project_id': project.id,
                })
            print("tt", milestones[milestone])

            task = milestones[milestone]

            Task.create({
                'name': f"Milestone {milestone} - {line.product_id.name}",
                'project_id': project.id,
                'parent_id': task.id,
            })

            # self.is_clicked = True


    def action_update_project(self):
        # project = Project.search([('name', '=', self.name)])

        tasks = self.env['project.task'].search(['project_id','=', self.id])
        tasks.unlink()

        Project = self.env['project.project']
        Task = self.env['project.task']

        project = Project.search([('name', '=', self.name)])

        # project = Project.create({
        #     'name': self.name,
        #     'partner_id': self.partner_id.id,
        #     # 'project_id': order.id,
        # })

        self.project_id = project.id

        print(project.name)

        milestones = {}
        for line in self.order_line:

            milestone = line.milestone

            if milestone not in milestones:
                milestones[milestone] = Task.create({
                    'name': f"Milestone {milestone}",
                    'project_id': project.id,
                })
            print("tt", milestones[milestone])

        task = milestones[milestone]

        Task.create({
            'name': f"Milestone {milestone} - {line.product_id.name}",
            'project_id': project.id,
            'parent_id': task.id,
        })

        # Project = self.env['project.project']
        Task = self.env['project.task']


        for line in self.order_line:
            milestone = line.milestone

            # project = Project.browse(order.id)
            project = Project.search([('name', '=', self.name)])
            print(project)

            # tasks = Task.search([('project_id', '=', project),('name', '=', f"Milestone {milestone}")])
            sub_task = Task.search([('project_id', '=', project),('name', '=', f"Milestone {milestone} - {line.product_id.name}"),('parent_id', '=', f"Milestone {milestone}")])

            # print("iiiii", tasks)
            # print("lllllll", sub_task)

            if not sub_task and not tasks:
               task = Task.create({
                   'name': f"Milestone {milestone}",
                   'project_id': project.id,
               })
               sub_task = Task.create({
                   'name': f"Milestone {milestone} - {line.product_id.name}",
                   'project_id': self.project_id.id,
                   'parent_id': task.id,
               })
               print("lll")
               print(sub_task)


               # sub_task = Task.create({
               #     'name': f"Milestone {milestone} - {line.product_id.name}",
               #     'project_id': project.id,
               #     'parent_id': tasks.id,
               # })

               print("kk")
               print(sub_task.name)
               print(sub_task.parent_id.name)


