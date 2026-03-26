import warnings
warnings.filterwarnings('ignore')

import sqlite3
import json
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import ollama

app = Flask(__name__)
DATABASE = "fashion.db"


# ---------------- DB ---------------- #
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            response TEXT,
            created_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            color TEXT,
            style TEXT,
            budget TEXT,
            occasion TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- MEMORY ---------------- #
def extract_preferences(text):
    text = text.lower()

    colors = ["black","white","blue","red","green","yellow","pink","grey"]
    styles = ["casual","formal","party","ethnic"]
    budgets = ["low","medium","high"]
    occasions = ["office","wedding","party","travel"]

    data = {"color":None,"style":None,"budget":None,"occasion":None}

    for c in colors:
        if c in text: data["color"]=c
    for s in styles:
        if s in text: data["style"]=s
    for b in budgets:
        if b in text: data["budget"]=b
    for o in occasions:
        if o in text: data["occasion"]=o

    return data


def save_memory(pref):
    conn = get_db()
    conn.execute("INSERT INTO memory (color,style,budget,occasion) VALUES (?,?,?,?)",
                 (pref["color"],pref["style"],pref["budget"],pref["occasion"]))
    conn.commit()
    conn.close()


def get_memory():
    conn = get_db()
    row = conn.execute("SELECT * FROM memory ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()

    if not row:
        return "No preferences yet"

    return f"Color:{row['color']} Style:{row['style']} Budget:{row['budget']} Occasion:{row['occasion']}"


# ---------------- SAFE PARSE ---------------- #
def normalize_list(lst):
    out=[]
    for i in lst:
        if isinstance(i,dict):
            out.append(i.get("name") or i.get("item") or i.get("value") or str(i))
        else:
            out.append(i)
    return out


# ---------------- AI ---------------- #
def generate_ai_response(user_input):

    prompt=f"""
    You are a fashion stylist.

    Memory:
    {get_memory()}

    Request:
    {user_input}

    ONLY RETURN JSON:
    {{
      "items": ["item1"],
      "accessories": ["acc1"],
      "fashion_tip": "",
      "description": "",
      "confidence": "High"
    }}
    """

    try:
        res = ollama.chat(
            model='phi3:mini',
            messages=[{"role":"user","content":prompt}]
        )

        txt = res['message']['content']
        txt = re.sub(r"```json|```","",txt).strip()

        match = re.search(r"\{.*\}", txt, re.DOTALL)
        if match:
            txt = match.group()

        data = json.loads(txt)

    except Exception as e:
        print("AI ERROR:", e)
        data = {
            "items":["T-shirt","Jeans"],
            "accessories":["Watch"],
            "fashion_tip":"Keep it simple",
            "description":"Fallback suggestion",
            "confidence":"Low"
        }

    data["items"]=normalize_list(data.get("items",[]))
    data["accessories"]=normalize_list(data.get("accessories",[]))

    return data


# ---------------- ROUTES ---------------- #
@app.route("/", methods=["GET","POST"])
def home():
    conn = get_db()

    if request.method=="POST":

        user_input = request.form.get("message")

        if not user_input:
            category=request.form.get("category")
            style=request.form.get("style")
            occasion=request.form.get("occasion")
            season=request.form.get("season")
            budget=request.form.get("budget")
            color=request.form.get("color")

            user_input=f"{category} {style} outfit for {occasion} in {season} with {color} under {budget}"

        pref = extract_preferences(user_input)
        save_memory(pref)

        result = generate_ai_response(user_input)

        conn.execute("INSERT INTO chats (user_input,response,created_at) VALUES (?,?,?)",
                     (user_input,json.dumps(result),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

    rows = conn.execute("SELECT * FROM chats").fetchall()
    conn.close()

    chats=[]
    for r in rows:
        try:
            resp=json.loads(r["response"])
        except:
            resp={"description":r["response"]}

        chats.append({"user":r["user_input"],"bot":resp})

    return render_template("index.html", chats=chats)


@app.route("/history")
def history():
    conn=get_db()
    rows=conn.execute("SELECT * FROM chats ORDER BY id DESC").fetchall()
    conn.close()

    chats=[]
    for r in rows:
        try:
            resp=json.loads(r["response"])
        except:
            resp={"description":r["response"]}

        chats.append({"user":r["user_input"],"bot":resp})

    return render_template("history.html", chats=chats)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/clear")
def clear():
    conn=get_db()
    conn.execute("DELETE FROM chats")
    conn.execute("DELETE FROM memory")
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


if __name__=="__main__":
    init_db()
    app.run()