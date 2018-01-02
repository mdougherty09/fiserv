def customize_installer_files(apps='all',validate='true'):
    """
    apps='all',validate='true'
    * Argument list provided to be displayed using fab -l; manually manitain if any options change
    """
    validate= 'true'==validate.lower()

    _set_applications(apps)

    if validate and not validate_config(apps,use_downloaded_artifacts=True):
        cont = fabric.operations.prompt("validate_config failed.  Are you sure you want to continue?",default="N",validate='^[YyNn]$')
        if 'N'==cont or 'n'==cont:
            puts('Aborting customize_insatller_files.')
            return

    for app in _get_installer_apps():
        if _host_specific_installer(app):
            for hostname in _get_stripped_servers(app):
                puts("customizing installer for "+app+" on host "+hostname)
                host_base_path = env.artifact_root + '/' + app + '/' + hostname
                if not os.path.exists(host_base_path):
                    puts('Creating directory '+host_base_path)
                    os.mkdir(host_base_path)
                for file_path in _get_artifacts(app):
                    file_name = _get_file_name(file_path)
                    shutil.copy(env.artifact_root + '/' + app + '/' + file_name,host_base_path)
                _customize_autoinstaller(app,host_base_path,hostname)
        else:
            puts("customizing installer for "+app)
            _customize_autoinstaller(app,env.artifact_root + app)
