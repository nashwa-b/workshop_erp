# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    """Extends sales model to import lines"""
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project')

    def action_create_project_sale(self):
        for record in self:

            pr = self.env['project.project'].create({
                'name': record.name,
                'task_ids': [fields.Command.create({
                    'name': f"Milestone {line.milestone}",
                }) for line in record.order_line],
            })

            tasks = self.env['project.task'].search([('project_id', '=', pr.id)])
            print(tasks)

            milestone = {}

            # milestone = line.milestone

            for line in record.order_line:
                tasks.create({
                    'name': record.name,
                    'project_id': pr.id,
                    'child_ids': [fields.Command.create({
                        # 'name': f"Milestone: {line.milestone} - {line.product_id.id}",
                        'name': f"Milestone: {line.product_id.name}",
                        # 'milestone_id': line.milestine.id
                        # 'product_id': line.product_id.id,

                    })],
                })




        # for record in self:
        #     project = self.env['project.project']
        #     task = self.env['project.task']
        #     pr = project.create({
        #         'name': record.name
        #     })
        #
        #     milestones = {}
        #
        #     milestone = line.milestone
        #
        #     milestones[milestone] = task.create({
        #         'name': f"Milestone {line.milestone}",
        #     })
        #
        #
        #     for line in record.order_line:
        #         print(line)
        #         pr.task_ids.create({
        #                 'name': f"Milestone {line.milestone}",
        #                 # 'child_ids': [fields.Command.create({'name': f"Milestone: {line.milestone} - {line.product_id.id}"})]
        #                 # 'milestone_id': line.milestine.id
        #                 # 'product_id': line.product_id.id,
        #             }),
        #         print("llll",pr.task_ids)
        #         print(task.name)

                # pr = self.env['project.project'].create({
                #     'name': record.name,
                #     'task_ids': [fields.Command.create({
                #         'name': f"Milestone {line.milestone}",
                #         # 'milestone_id': line.milestine.id
                #         # 'product_id': line.product_id.id,
                #     }) for line in record.order_line],
                # })

                # self.env['project.task'].create({
                #
                #     'child_ids': [fields.Command.create({
                #         'name': f"Milestone: {line.milestone} - {line.product_id.id}",
                #         # 'milestone_id': line.milestine.id
                #         # 'product_id': line.product_id.id,
                #
                #     })],
                # })

            # for record in self:
            #     record.project_id = project.id
            #     project.create({
            #         'name': record.name,
            #         # 'project_id': record.project_id,
            #     })
            #
            #     tasks = self.env['project.task'].browse(record.project_id)
            #     for line in record.order_line:
            #
            #         tasks.create({
            #             'name': f"Milestone: {line.milestone} - {line.product_id.id}",
            #             'project_id': record.id,
            #             # 'project_id': record.id,
            #             'parent_id': project.id,
            #             # 'child_ids': [fields.Command.create({
            #             #     'name': f"Milestone: {line.milestone} - {line.product_id.id}",
            #             # })],
            #         })

                    # })
                    #
                    #
                    # proj = self.env['project.project'].search([('name', '=', record.name)],limit=1)
                    # print('proj', proj)
                    #
                    # # 'task_ids': [fields.Command.write(existing_task_id, {'name': 'Updated Task Name'})]
                    #
                    # proj.create({
                    #     'name':record.name,
                    #     'task_ids': [fields.Command.create({
                    #         'name': f"Milestone {line.milestone}",
                    #
                    #         # 'milestone_id': line.milestine.id
                    #         # 'product_id': line.product_id.id,
                    #
                    #     })],
                    #
                    # })
                    #
                    # tasks =  self.env['project.task'].search([('project_id.name', '=', record.name)])
                    #
                    # tasks.write({
                    #     'name': f"Milestone {line.milestone}",
                    #     'child_ids': [fields.Command.create({
                    #          'name': f"Milestone: {line.milestone} - {line.product_id.id}",
                    #     })],
                    # })
                    #
                    #



                    # 'child_ids': [fields.Command.create({
                    #     'name': f"Milestone: {line.milestone} - {line.product_id.id}",
                    #     # 'milestone_id': line.milestine.id
                    #     # 'product_id': line.product_id.id,
                    #
                    # })],






