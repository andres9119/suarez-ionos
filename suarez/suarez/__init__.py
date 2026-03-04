try:
    import pymysql
    pymysql.install_as_MySQLdb()
    # Bypass MySQL version check for Django 6.0 compatibility with pymysql
    pymysql.version_info = (8, 0, 11, "final", 0)
except ImportError:
    pass
