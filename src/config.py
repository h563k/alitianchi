import yaml
import argparse


class ModelConfig:

    def __init__(self) -> None:
        self.args = self.args_read()
        self.save_path = self.config_read()['model']['save_path']
        self.model_path = self.config_read()['model']['model_path']
        self.embedding_path = self.config_read()['model']['embedding_path']
        self.json_file_path = self.config_read()['model']['json_file_path']
        self.full_embedding_path = f'{self.save_path}/{self.embedding_path}'
    # 创建 ArgumentParser 对象

    def args_read(self):
        parser = argparse.ArgumentParser(description='这是一个示例程序。')
        # 添加参数
        parser.add_argument('--save_path', type=bool)
        parser.add_argument('--model_path', type=bool)
        parser.add_argument('--full_path', type=bool)
        # 解析命令行参数
        args = parser.parse_args()
        return args

    def config_read(self):
        with open('scripts/setting.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config

    def shell_response(self):
        if self.args.save_path:
            return self.save_path
        elif self.args.model_path:
            return self.model_path
        elif self.args.full_path:
            return f'{self.save_path}/{self.model_path}'
        else:
            print("请输入参数")


def main():
    model_config = ModelConfig()
    print(model_config.shell_response())


if __name__ == '__main__':
    main()
