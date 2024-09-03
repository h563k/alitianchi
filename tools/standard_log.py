import re
import logging
import functools


def log_to_file(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 获取函数名称作为日志文件名的基础
        log_filename = f"log/{func.__name__}.log"

        # 配置日志
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        logger = logging.getLogger(func.__name__)
        # 开始记录日志
        logger.info(f"函数 '{func.__name__}' 开始运行.")

        # 执行函数
        result = func(*args, **kwargs)
        logger.info(result)

        return result

    return wrapper

# 示例使用


if __name__ == "__main__":
    @log_to_file
    def example_function():
        print("This is some output.")
        return "Function executed successfully."

    # 调用被装饰的函数
    result = example_function()
    print(f"Result: {result}")
