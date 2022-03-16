# See http://docs.gunicorn.org/en/latest/settings.html for a list of available
# settings. Note that the setting names are used here and not the CLI option
# names (e.g. "pidfile", not "pid").

# Set some sensible Gunicorn options, needed for things to work with Nginx
pidfile = "/run/gunicorn/gunicorn.pid"
bind = "unix:/run/gunicorn/gunicorn.sock"
# umask working files (worker tmp files & unix socket) as 0o117 (i.e. chmod as
# 0o660) so that they are only read/writable by wagtail and nginx users.
umask = 0o117
# Set the worker temporary file directory to /run/gunicorn (rather than default
# of /tmp) so that all of Gunicorn's files are in one place and a tmpfs can be
# mounted at /run for better performance.
# http://docs.gunicorn.org/en/latest/faq.html#blocking-os-fchmod
worker_tmp_dir = "/run/gunicorn"
