from odoo import http
from odoo.http import request
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ApplicationForm(models.Model):
    _name = 'application.form'
    _description = 'Application Form'

    name = fields.Char(string="Company Name", required=True, translate=True)
    contact_name = fields.Char(string="Contact Name", required=True, translate=True)
    email = fields.Char(string="Email", required=True, translate=True)
    phone_number = fields.Char(string="Phone Number", required=True, translate=True)
    Circle = fields.Selection(
        [
            ('option-1', 'Circle 1'),
            ('option-2', 'Circle 2'),
            ('option-3', 'Circle 3'),
        ],
        string="Circle",
        required=True,
    )
    description = fields.Text(string="Description",required=True, translate=True)
    file_upload = fields.Binary(string="File Upload", attachment=True,required=True, translate=True)
    file_name = fields.Char(string="File Name",required=True, translate=True)


class MdaController(http.Controller):
    # @http.route('/', auth='public', website=True)
    # def homepage_view(self, **kwargs):
    #     return request.render('mda.homepage_template',{})
    #
    # @http.route('/contactus', type='http', auth='public', website=True)
    # def contact_us_form(self, **kwargs):
    #     return request.render('mda.contact_us_template', {})
    @http.route('/', auth='public', website=True)
    def homepage_view(self, **kwargs):
        direction = "rtl" if "/ar/" in request.httprequest.path else "ltr"
        return request.render('mda.homepage_template', {'direction': direction})

    @http.route('/contactus', type='http', auth='public', website=True)
    def contact_us_form(self, **kwargs):
        direction = "rtl" if "/ar/" in request.httprequest.path else "ltr"
        return request.render('mda.contact_us_template', {'direction': direction})

    @http.route('/contactus/submit', type='http', auth='public', website=True, csrf=False, methods=['POST'])
    def contact_us_submit(self, **post):
        try:
            # Save the submitted details into the application.form model
            request.env['application.form'].sudo().create({
                'name': post.get('name'),
                'contact_name': post.get('contact_name'),
                'email': post.get('email'),
                'phone_number': post.get('phone_number'),
                'Circle': post.get('Circle'),
                'description': post.get('description'),
                'file_name': post.get('file').filename if 'file' in post else None,
                'file_upload': post.get('file').read() if 'file' in post else None,
            })
            return request.render('mda.contact_us_success')
        except Exception as e:
            return request.render('mda.contact_us_failure', {'error': str(e)})