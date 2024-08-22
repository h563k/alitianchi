from langchain.prompts import PromptTemplate

# 定义你的自定义prompt模板

template_1 = """
### 临床资料
{clinical_information}
###信息抽取
核心临床信息:
"""

template_2 = """
### 临床资料
{clinical_information}
### 病机选项
{pathogenesis_options}
### 病机答案
病机答案:
"""
template_3 = """
### 临床资料
{clinical_information}
### 证候选项
{syndrome_options}
### 证候答案
证候答案: 
"""
template_4 = """
### 临床资料:
{clinical_information}
### 临证体会
临证体会: 
"""


def custom_prompt(data, type):
    # 输出构造好的prompt
    # 构造prompt输入
    if type == "task_1":
        inputs = {
            "clinical_information": data["临床资料"]
        }
        PROMPT = PromptTemplate(
            template=template_1,
            input_variables=["clinical_information"]
        )
        return PROMPT.format(**inputs)
    elif type == "task_2":
        inputs = {
            "clinical_information": data["临床资料"],
            "pathogenesis_options": data["病机选项"]
        }
        PROMPT = PromptTemplate(
            template=template_2,
            input_variables=["clinical_information", "pathogenesis_options"]
        )
        return PROMPT.format(**inputs)
    elif type == "task_3":
        inputs = {
            "clinical_information": data["临床资料"],
            "syndrome_options": data["证候选项"]
        }
        PROMPT = PromptTemplate(
            template=template_3,
            input_variables=["clinical_information", "syndrome_options"]
        )
        return PROMPT.format(**inputs)
    elif type == "task_4":
        inputs = {
            "clinical_information": data["临床资料"],
        }
        PROMPT = PromptTemplate(
            template=template_4,
            input_variables=["clinical_information"]
        )
        return PROMPT.format(**inputs)


if __name__ == "__main__":
    # 示例数据
    data = {
        "案例编号": "病例247",
        "临床资料": "某女，62岁。初诊：1957年1月。主诉及病史：发病十数天，咳逆不能平卧，唾白色泡沫痰。诊查：短气，语音低微，神识昏愦不清，时妄言语，终又复言，身有微热，手足厥冷，偶饮热一二口。脉浮细数而无力。",
        "病机答案": "",
        "病机选项": "A:痰浊;B:耗损心气和心阴;C:食郁于胃;D:少阴伤寒;E:心移热于小肠;F:气阴两亏;G:脾胃湿热;H:阴虚内热;I:肾水不足;J:心气虚",
        "证候答案": "",
        "证候选项": "A:风湿内侵;B:气虚血瘀;C:血虚生风;D:肾元不固;E:虚火牙痛;F:肝气横逆;G:阴亏之体;H:感暑邪;I:复感外邪;J:阴寒内盛",
        "临证体会": ""
    }
    print(custom_prompt(data, 'task_1'))
