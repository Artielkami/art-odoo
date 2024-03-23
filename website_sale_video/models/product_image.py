from odoo import fields, models, api, _
from odoo.addons.web_editor.tools import get_video_embed_code
from ..tools import get_local_video_embed_code


class ProductImage(models.Model):
    _inherit = 'product.image'

    video_attachment_id = fields.Binary(attachment=True)
    use_system_video = fields.Boolean()
    video_show_controls = fields.Boolean(string="Show Controls", default=True)
    video_auto_play = fields.Boolean(string="Auto play", help="If auto play on, video is muted")

    @api.depends('video_url', 'video_attachment_id')
    def _compute_embed_code(self):
        for image in self:
            video_url = image.video_url or f'{image.get_base_url()}/web/content/product.image/{image.id}/video_attachment_id'
            if not image.video_attachment_id:
                embed_code = get_video_embed_code(video_url) or False
            else:
                options = ['loop']
                options.append('muted autoplay' if image.video_auto_play else '')
                options.append('controls' if image.video_show_controls else '')
                embed_code = get_local_video_embed_code(video_url, ' '.join(options))
            image.embed_code = embed_code

    @api.model_create_multi
    def create(self, vals_list):
        images = super().create(vals_list)
        for image in images.filtered(lambda x: x.video_attachment_id):
            image._write({'video_url': f'{image.get_base_url()}/web/content/product.image/{image.id}/video_attachment_id'})
        return images
