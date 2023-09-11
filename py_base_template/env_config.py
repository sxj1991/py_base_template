import json

from environ import environ

config = None


def get_env():
    """
    读取配置文件数据方法
    不同配置文件单独信息可由 config.get('CONFIG','') 读取
    """
    global config
    # 可根据传入参数获取不同环境变量属性值
    env_name = environ.Env().str('PROJECT_ENV', 'dev')
    # 根据环境变量参数读取不同配置文件
    read_file = environ.Path('../config/.env_' + env_name + '_setting.json').root
    with open(read_file, 'r', encoding='utf-8') as f:
        # 读取配置文件 转成json
        config = json.load(f)

    return config


if __name__ == '__main__':
    get_env()