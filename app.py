import os
from dotenv import load_dotenv
import streamlit as st
#from openai import OpenAI  # for OpenAI API
from langchain_openai import ChatOpenAI                     # for LangChain
from langchain.schema import HumanMessage, SystemMessage    # for LangChain

# 環境変数の読み込み(モジュール読み込み時に 1回だけ実行される)
load_dotenv()

class Config:
    MODEL_NAME = "gpt-4o-mini"      # "gpt-3.5-turbo"
    TEMPERATURE = 0

def get_api_key():
    # 環境変数からAPIキーを取得する関数
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("APIキーが見つかりません。環境変数にOPENAI_API_KEYを設定してください。")
    return api_key

class LlmHandler:
    def __init__(self, model_name, temperature, api_key):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key
        
        # < memo > 
        # ChatOpenAI は、APIキーを明示的に渡さなくても、内部で自動的に環境変数を探しにいく仕組み
        # -> api_key=openai_api_key の部分は省略可能
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature, api_key=self.api_key)
    
    def generate_response(self, input_message, expert_tema):
        response = self.llm(
                [
                    SystemMessage(content=f"You are a helpful assistant that is an expert in {expert_tema}. Provide sound advice on {expert_tema}-related questions."),
                    HumanMessage(content=input_message)
                ]
            )
        return response.content

def main():
    experts = {
        "犬": "dog",
        "猫": "cat"
    }
    
    display_expert_keys = [f"{key}の専門家" for key in list(experts.keys())]
    #print(display_expert_keys)

    api_key = get_api_key()
    if not api_key:
        return

    llm_handler = LlmHandler(model_name=Config.MODEL_NAME, temperature=Config.TEMPERATURE, api_key=api_key)

    st.title("専門家（LLM）に質問できるWeb相談アプリ")

    st.write("各分野のプロフェッショナルAIが質問に答えます。")
    st.write("質問したい専門家を選択し、質問内容を入力して「送信」ボタンを押してください。")
    st.write("for Chapter 6 【提出課題】LLM機能を搭載したWebアプリ")
    st.divider()

    selected_item = st.radio(
        "**質問したい専門家を選択してください。**",
        #["犬の専門家", "猫の専門家"]
        display_expert_keys
    ).split("の")[0]  # "犬の専門家" -> "犬" に変換
    st.divider()

    if selected_item in experts:
        expert_tema = experts[selected_item]
        st.write(f"**{selected_item}の専門家**が選択されています。")
        input_message = st.text_area(label=f"**「{selected_item}」** に関する質問を入力してください。")
        
        if st.button("送信"):
            st.divider()

            result_message = llm_handler.generate_response(input_message=input_message, expert_tema=expert_tema)
            st.write(f"**{selected_item}の専門家の回答 :**")
            st.write(f"{result_message}")

if __name__ == "__main__":
    main()