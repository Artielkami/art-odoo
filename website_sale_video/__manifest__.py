{
    'name': "Website Sale Video",
    'description': "Insert video in website editor and product video",
    'author': "Artiel",
    'category': 'Website',
    'sequence': 300,
    'version': '1.0',
    'depends': ['website_sale'],
    'data': [
        'views/product_image.xml'
    ],
    'assets': {
        'web_editor.assets_media_dialog': [
            'website_sale_video/static/src/components/document_selector.js',
        ],
    }
}
