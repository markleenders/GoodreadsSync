from calibre.srv.routes import endpoint, json

@endpoint('/grsync/get_profile_names', auth_required=False, postprocess=json)
def grsync_get_profile_names(ctx, rd):
    import traceback
    traceback.print_stack()

    import calibre_plugins.goodreads_sync.config as cfg

    users = cfg.plugin_prefs[cfg.STORE_USERS]
    print("GRSYNC %s" % str(users))

    return [*users]

@endpoint('/grsync/add_remove_book_to_shelf', auth_required=False)
def grsync_add_remove_book_to_shelf(ctx, rd):
    import traceback
    traceback.print_stack()

    from calibre_plugins.goodreads_sync.core import HttpHelper

    goodreads_id = rd.query.get('goodreads_id', None)
    if goodreads_id is None:
        return b'missing goodreads_id'

    profile_name = rd.query.get('profile_name', None)
    if profile_name is None:
        return b'missing profile_name'

    shelf_name = rd.query.get('shelf_name', None)
    if shelf_name is None:
        return b'missing shelf_name'

    action = rd.query.get('action', None)
    if action is None:
        return b'missing action'

    grhttp = HttpHelper()
    print("GRSYNC %s" % str(grhttp))
    client = grhttp.create_oauth_client(profile_name)
    grhttp.add_remove_book_to_shelf(client, shelf_name, goodreads_id, action)

    return b'grsync'

@endpoint('/grsync/update_reading_progress', auth_required=False)
def grsync_update_reading_progress(ctx, rd):
    import traceback
    traceback.print_stack()

    from calibre_plugins.goodreads_sync.core import HttpHelper

    goodreads_id = rd.query.get('goodreads_id', None)
    if goodreads_id is None:
        return b'missing goodreads_id'

    percent = rd.query.get('percent', None)
    if percent is None:
        return b'missing percent'

    profile_name = rd.query.get('profile_name', None)
    if profile_name is None:
        return b'missing profile_name'

    grhttp = HttpHelper()
    print("GRSYNC %s" % str(grhttp))
    client = grhttp.create_oauth_client(profile_name)
    #grhttp.add_remove_book_to_shelf(client, "currently-reading", goodreads_id, 'add')
    grhttp.update_status(client, goodreads_id, percent)

    return b'grsync'

