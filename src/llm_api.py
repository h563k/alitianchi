import re
from http import HTTPStatus
import dashscope
from openai import OpenAI
from tools.config import ModelConfig
from tools.standard_log import log_to_file


def llm_qwen(prompt, model_name) -> str:
    config = ModelConfig()
    dashscope.api_key = config.dashscope_key
    response = dashscope.Generation.call(
        model=model_name,
        prompt=prompt,
        seed=42,
        top_p=0.8,
        result_format='message',
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        repetition_penalty=1.0
    )
    if response.status_code == HTTPStatus.OK:
        return response['output']['choices'][0]['message']['content']
    else:
        return 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        )


def llm_huatuo(type, role_content, model_name) -> str:
    client = OpenAI(base_url="http://127.0.0.1:9997/v1",
                    api_key="not used actually")
    if type == 'task_3':
        system_content = """请根据临床资料，选出合适的病机(单选或多选)，只需要给出答案，不需要任何额外回答,格式如下：
            病机：
        """
    # role_content = """### 临床资料
    #     谭某，男，9岁:初诊:1977年1月8日。主诉及病史:患儿于1岁9个月时突然发热、浮肿，当时诊为急性肾炎。以后曾在多所医院住院治疗，诊为慢性肾炎，曾用中西药物而疗效不显。后来家长失去信心，不再予治疗。1976年12月底，患儿发热、咳嗽，以后出现嗜睡、鼻衄、恶心、呕吐、尿少，于1977年1月某日急诊入院。入院时体检:明显消瘦，皮肤干燥，鼻翼煽动，呼吸困难，心律不齐。实验室检查:二氧化碳结合力12.2容积%，尿素氮216mg%，血色素5.8g，诊断为慢性肾炎、尿毒症、酸中毒、继发性贫血。入院后立即输液、纠正酸中毒及脱水;予抗生素和中药真武汤、生脉散加味方，症状稍有稳定，二氧化碳结合力上升至56容积%，但全身症状无大改善，仍处于嗜睡衰竭状态，同时有鼻衄、呕吐咖啡样物。1月6日血色素降至4.5g，当时曾予输血。1月7日患儿情况转重，不能饮食，恶心呕吐频频发作，服药亦十分困难;大便1日数次，呈柏油样便;并有呕血、呼吸慢而不整(14~18次/分)，心率减至60~65次/分，当即予可拉明、洛贝林、生脉散注射液交替注射。1月8日，患儿继续呈嗜睡衰竭状态，面色晦暗，呼吸减慢，心率减慢至60次/分，大便仍为柏油便，情况越来越重，因急请会诊。诊查:会诊时，患儿呈嗜睡朦胧状态，时有恶心呕吐，呼吸深长而慢，脉沉细微弱无力而迟，舌嫩润齿痕尖微赤，苔薄白干中心微黄。
    #     ### 病机选项
    #     A:热结阳明;B:风阳上升;C:疫毒乘虚内侵中焦;D:冲任受损;E:气血两虚;F:心移热于小肠;G:气阴两虚;H:脾胃败绝;I:肠道传导失司;J:痰浊
    # """
        response = client.chat.completions.create(
            model=model_name,
            temperature=0,
            max_tokens=100,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": role_content}
            ],
        )
        return response.choices[0].message.content


@log_to_file
def local_openai(prompt, model_name=None) -> str:
    config = ModelConfig()
    model_name = model_name if model_name else config.model_name
    if re.findall(r'qwen', model_name):
        return llm_qwen(prompt, model_name)
    elif re.findall(r'huatuo', model_name):
        return 'huatuo'
    else:
        return '请选择合适模型'
