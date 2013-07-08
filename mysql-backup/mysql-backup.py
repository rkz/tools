#!/usr/bin/python
"""
MySQL databases backup script

Usage:   mysql-backup.py

Configuration:
- copy config.py.dist to config.py (alongside mysql-backup.py)

"""

from datetime import datetime, timedelta
import os
import config

today = datetime.now().strftime('%Y-%m-%d')
oldest = datetime.now() - timedelta(config.MAX_AGE)

for database in config.DATABASES:

    # Dump the database to an SQL file
    backup_file = '%s/%s.%s.sql' % (config.BACKUP_DIRECTORY, database, today)
    command = 'mysqldump -u%s -p%s %s >%s' \
              % (config.MYSQL_USER, config.MYSQL_PASSWD, database, backup_file)

    print 'Backing up database %s to %s' % (database, backup_file)
    os.system(command)

    # Delete backups of this database older than MAX_AGE
    current_backups = os.listdir(config.BACKUP_DIRECTORY)
    deleted_backups = []
    for backup in current_backups:
        path = config.BACKUP_DIRECTORY + '/' + backup
        modified = datetime.fromtimestamp(os.path.getmtime(path))
        if (backup.find(database) != -1) and (modified < oldest):
            os.system('rm ' + path)
            deleted_backups.append(backup)

    if len(deleted_backups) > 0:
        print 'Deleted old backups : ' + ', '.join(deleted_backups)

    print ''

print 'All backups done.'
print ''
