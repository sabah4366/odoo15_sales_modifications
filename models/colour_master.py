from odoo import  models,api,fields

class ColourMaster(models.Model):
    _name = 'sales_task.color'
    _description = 'Colour '

    colour_name=fields.Char(string="Colour Name",store=True)
    job_number=fields.Char(string="Job Number",store=True)
    color_widget=fields.Integer(string='Color')


    def name_get(self):
        return [(record.id, ' %s' % (record.colour_name)) for record in self]