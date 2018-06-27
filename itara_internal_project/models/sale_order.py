from odoo import api,fields,models


class sale_order_line(models.Model):
    _inherit = "sale.order.line"
    
    due_date = fields.Date('Due Date')

    def _timesheet_create_task_prepare_values(self):
        self.ensure_one()
        project = self._timesheet_find_project()
        planned_hours = self._convert_qty_company_hours()
        code = self.env['ir.sequence'].sudo().next_by_code('project.task')
        value = {
            'name': '%s:%s' % (self.order_id.name or '', self.name.split('\n')[0] or self.product_id.name),
            # 'code': "/",
            'planned_hours': planned_hours,
            'remaining_hours': planned_hours,
            'partner_id': self.order_id.partner_id.id,
            'description': self.name + '<br/>',
            'project_id': project.id,
            'sale_line_id': self.id,
            'company_id': self.company_id.id,
            'user_id': False, # force non assigned task, as created as sudo()
            'date_deadline':self.due_date,

        }
        print (value)
        return value

class ProjectTask(models.Model):
    _inherit = "project.task"


    code = fields.Char(
        string='Task Number', default="/", readonly=True)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    due_date = fields.Date(related='order_line.due_date',string='Due Date')
    
    
class Lead(models.Model):
    _inherit = "crm.lead"
    
        
    @api.onchange('team_id')
    def onchange_team_id(self):
        vals = {}
        user = []
        if self.team_id:
            sec = self.env['crm.team'].browse(self.team_id.id)
            for sec_line in sec.member_ids:
                user.append(sec_line.id)
        domain = [('id','=', user)]
        vals = {'domain': {'user_id' : domain}, 'value' : {'user_id' : False}}
        return vals
    
    
    
    
