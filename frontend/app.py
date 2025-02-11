import streamlit as st
import os
from urllib.parse import quote
from streamlit.runtime.scriptrunner import get_script_run_ctx

def main():
    # セッションIDを取得
    session_id = get_script_run_ctx().session_id
    st.sidebar.info(f"Session ID:  \n{session_id}")

    # バックエンドのURLを環境変数から取得（デフォルトはローカル開発用）
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

    # ポータルサイトの定義
    portal_sites = [
        {"name": "Google", "url": "https://www.google.co.jp", "description": "世界最大の検索エンジン"},
        {"name": "Yahoo! JAPAN", "url": "https://www.yahoo.co.jp", "description": "日本の総合ポータルサイト"},
        {"name": "MSN", "url": "https://www.msn.com/ja-jp", "description": "マイクロソフトのポータルサイト"},
        {"name": "goo", "url": "https://www.goo.ne.jp", "description": "NECビッグローブが運営するポータル"},
        {"name": "楽天", "url": "https://www.rakuten.co.jp", "description": "ショッピングとサービスの総合サイト"}
    ]

    # Markdownテーブルの作成
    table_rows = ["| サイト名 | 説明 | URL |", "|----------|------|-----|"]
    
    for site in portal_sites:
        # URLエンコードしてFastAPIのリダイレクトエンドポイントを作成
        encoded_url = quote(site['url'])
        encoded_name = quote(site['name'])
        redirect_url = f"{BACKEND_URL}/api/redirect/{encoded_name}?url={encoded_url}&session_id={session_id}"
        
        # テーブル行を作成
        table_rows.append(
            f"| {site['name']} | {site['description']} | [{site['name']}]({redirect_url}) |"
        )
    
    st.markdown("\n".join(table_rows))

if __name__ == "__main__":
    main()