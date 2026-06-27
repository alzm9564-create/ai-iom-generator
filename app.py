from flask import Flask, render_template, request, redirect, Response

from openai import OpenAI
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("iom.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        spec TEXT,
        usage TEXT,
        result TEXT
    )
    """)

    conn.commit()

    conn.close()


def generate_doc(client, product, spec, usage):

    prompt = f"""
你是一位資深機械工程師，請撰寫正式工程文件（IOM），需符合工業文件標準。

【輸入資料】
產品名稱：{product}
規格：{spec}
使用情境：{usage}

【輸出要求】
請使用條列與技術語言，避免口語化描述。

請依照以下格式輸出：

一、產品概述
- 說明產品功能與定位

二、技術規格
- 列出關鍵規格數據（電壓、功率、尺寸等）

三、操作與應用說明
- 實際應用場景
- 操作方式

四、風險與注意事項
- 使用風險
- 安全建議

請內容具體、專業，不要出現「這是一個很好的產品」等模糊描述。
"""


    response = client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[
            {"role": "system", "content": "你是工業技術文件工程師"},

            {"role": "user", "content": prompt}
        ],

        temperature=0.2
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":
        api_key = request.form["api_key"]
        client = OpenAI(api_key=api_key)

        product = request.form["product"]
        spec = request.form["spec"]
        usage = request.form["usage"]

        result = generate_doc(client, product, spec, usage)

        conn = sqlite3.connect("iom.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO records (product, spec, usage, result) VALUES (?, ?, ?, ?)",
            (product, spec, usage, result)
        )

        conn.commit()


        cursor.execute("""
        DELETE FROM records
        WHERE id NOT IN (
            SELECT id FROM records ORDER BY id DESC LIMIT 50
        )
        """)

        conn.commit()
        conn.close()


    conn = sqlite3.connect("iom.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, product, spec, usage, result FROM records ORDER BY id DESC")
    
    records = cursor.fetchall()

    conn.close()

    return render_template("index.html", result=result, records=records)


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("iom.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM records WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/download/<int:id>")
def download(id):

    conn = sqlite3.connect("iom.db")
    cursor = conn.cursor()

    cursor.execute("SELECT result FROM records WHERE id=?", (id,))

    data = cursor.fetchone()

    conn.close()

    return Response(
        data[0],

        mimetype="text/plain",

        headers={
            "Content-Disposition": f"attachment;filename=iom_{id}.txt"
        }
    )

if __name__ == "__main__":
    init_db()

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))