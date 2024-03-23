from markupsafe import Markup


def get_local_video_embed_code(video_url, options="muted autoplay loop"):
    """ Computes the valid iframe from given URL that can be embedded
        (or None in case of invalid URL).
    """
    # return Markup('<iframe class="embed-responsive-item" src="%s" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowFullScreen="true" frameborder="0"></iframe>') % (video_url,)
    return Markup('<video  class="embed-responsive-item" %s><source src="%s" type="video/mp4"></video> ') % (options, video_url,)

