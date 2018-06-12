from odoo import api,fields,models

class Project(models.Model):
    _inherit = 'project.project'
    
    state = fields.Selection([('inprogress','In progress'),('closed','Closed'), ('hold','Hold / Defered')],string = "State", default='inprogress')


    @api.multi
    def action_closed(self):
        self.write({'state': 'closed'})

    @api.multi
    def action_hold(self):
        self.write({'state': 'hold'})

    @api.multi
    def action_inprogress(self):
        self.write({'state': 'inprogress'})