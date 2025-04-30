import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

def generate_response(tokenizer, model, user_input, chat_history_ids=None):
    # 編碼用戶輸入並添加結束標記
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # 將新輸入追加到對話歷史
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
    
    # 生成回應
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8
    )
    
    # 解碼並返回回應
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

def main():
    tokenizer, model = load_model()
    chat_history_ids = None
    
    while True:
        # 從標準輸入讀取用戶輸入
        user_input = sys.stdin.readline().strip()
        if user_input.lower() == "exit":
            break
        
        # 生成回應
        response, chat_history_ids = generate_response(tokenizer, model, user_input, chat_history_ids)
        
        # 將回應寫入標準輸出
        print(response, flush=True)

if __name__ == "__main__":
    main()