# coding:utf-8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_web_xnysfc import app
from exts import db
manager = Manager(app)

#使用migrate绑定app和db
migrate = Migrate(app,db)

#添加迁移脚本的命令到manager
manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()


