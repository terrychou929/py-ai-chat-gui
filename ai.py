import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class AIChat:
    def __init__(self):
        # 初始化模型和分詞器
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        self.chat_history_ids = None

    def generate_response(self, user_input, chat_history_ids):
        # 編碼用戶輸入並添加結束標記
        new_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
        
        # 將新輸入追加到對話歷史
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
        
        # 生成回應
        chat_history_ids = self.model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.8
        )
        
        # 解碼回應
        response = self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response, chat_history_ids

    def update_chat_history(self, new_chat_history_ids):
        # 更新對話歷史
        self.chat_history_ids = new_chat_history_ids