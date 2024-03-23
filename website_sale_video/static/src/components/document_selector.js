/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { DocumentSelector } from "@web_editor/components/media_dialog/document_selector";

const _superCreateElements = DocumentSelector.createElements;

function isVideo(mimetype) {
    const videoMimeTypes = ["audio/mpeg", "video/x-matroska", "video/mp4", "video/webm"];
    return videoMimeTypes.includes(mimetype);
}

export async function _createVideoElement(attachment, orm) {
    const videoEl = document.createElement('video');
    let href = `/web/content/${encodeURIComponent(attachment.id)}?unique=${encodeURIComponent(attachment.checksum)}&download=true`;
    if (!attachment.public) {
        let accessToken = attachment.access_token;
        if (!accessToken) {
            [accessToken] = await orm.call(
                'ir.attachment',
                'generate_access_token',
                [attachment.id],
            );
        }
        href += `&access_token=${encodeURIComponent(accessToken)}`;
    }
    
    // videoEl.href = href;
    videoEl.innerHTML = `<source src="${href}" type="video/mp4">`;
    videoEl.title = attachment.name;
    videoEl.autoplay = true;
    videoEl.loop = true;
    videoEl.classList.add('h-100');
    videoEl.classList.add('w-100');
    // videoEl.dataset.mimetype = attachment.mimetype;
    return videoEl;
}

DocumentSelector._createVideoElement = _createVideoElement;

export async function createElements(selectedMedia, { orm }) {

    const videoAttachmentElements = {};
    for (let index = 0; index < selectedMedia.length; index++) {
        const attachment = selectedMedia[index];
        if (isVideo(attachment.mimetype)) {
            videoAttachmentElements[index] = await DocumentSelector._createVideoElement.apply(this, [attachment, orm])
        }
    }

    const resultDatas = await _superCreateElements.apply(this, [selectedMedia, { orm }]);
    if (Object.keys(videoAttachmentElements).length) {
        for (const index of Object.keys(videoAttachmentElements)) {
            resultDatas[index] = videoAttachmentElements[index];
        }
    }
    return Promise.all(resultDatas);
}

DocumentSelector.createElements = createElements;
DocumentSelector.mediaExtraClasses = DocumentSelector.mediaExtraClasses.concat(['w-100', 'w-75']);
