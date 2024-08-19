import os
import sys
import warnings
from src.rag_sample import rag_miedical

warnings.filterwarnings('ignore')
sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    promot = "你是一个中医专家，接下来会输入一个需要补全的评测，请按照格式补全‘病机答案’，‘证候答案’，‘临证体会’三部分，并尽可能的用中医知识回答"
    query = """
"案例编号": "病例247",
"临床资料": "某女，62岁。初诊：1957年1月。主诉及病史：发病十数天，咳逆不能平卧，唾白色泡沫痰。诊查：短气，语音低微，神识昏愦不清，时妄言语，终又复言，身有微热，手足厥冷，偶饮热一二口。脉浮细数而无力。",
"病机答案": "",
"病机选项": "A:痰浊;B:耗损心气和心阴;C:食郁于胃;D:少阴伤寒;E:心移热于小肠;F:气阴两亏;G:脾胃湿热;H:阴虚内热;I:肾水不足;J:心气虚",
"证候答案": "",
"证候选项": "A:风湿内侵;B:气虚血瘀;C:血虚生风;D:肾元不固;E:虚火牙痛;F:肝气横逆;G:阴亏之体;H:感暑邪;I:复感外邪;J:阴寒内盛",
"临证体会": ""
    """
    print(rag_miedical(query, promot))
