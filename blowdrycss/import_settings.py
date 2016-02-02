def import_settings():
    """ Imports the settings file.

    :return: None
    """
    try:
        import settings.blowdrycss_settings as settings                     # development case
    except ImportError:
        try:
            import blowdrycss_settings as settings                          # development "python setup.py test" case
        except ImportError:
            import blowdrycss.blowdrycss_settings as settings               # packaged deployment case