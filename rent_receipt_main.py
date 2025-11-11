import customtkinter as ctk
import os
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

project_dir = os.path.dirname(__file__)
db_path = os.path.join(project_dir, "ikoi_erp_db", "ikoi_erp.db")
pdf_dir = os.path.join(project_dir, "receipts_pdf")
os.makedirs(pdf_dir, exist_ok=True)

import sqlite3
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS rent_receipts
    (id INTEGER PRIMARY KEY, azukari_no TEXT, receipt_no TEXT, receipt_ym TEXT,
     payer_name TEXT, agent_name TEXT, amount INTEGER, rent_type TEXT, notes TEXT)''')
conn.commit()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("いこい住宅 預り証発行システム v2.0")
        self.geometry("650x850")

        ctk.CTkLabel(self, text="株式会社いこい住宅", font=("Bold", 28)).pack(pady=20)
        ctk.CTkLabel(self, text="預り証発行システム v2.0", font=("Bold", 18)).pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=40, fill="both", expand=True)

        self.entries = {}
        labels = ["受領年月:", "支払人名:", "代理人名:", "受領金額:", "備考:"]
        defaults = ["2025年11月分", "岡崎 一宏", "", "85000", "一部入金のため残額は後日請求"]
        for i, (label, default) in enumerate(zip(labels, defaults)):
            ctk.CTkLabel(frame, text=label).grid(row=i, column=0, padx=20, pady=15, sticky="w")
            if "備考" in label:
                widget = ctk.CTkTextbox(frame, height=100)
                widget.insert("0.0", default)
            else:
                widget = ctk.CTkEntry(frame, width=300)
                widget.insert(0, default)
            widget.grid(row=i, column=1, padx=20, pady=15)
            self.entries[label] = widget

        ctk.CTkLabel(frame, text="家賃内容:").grid(row=5, column=0, padx=20, pady=15, sticky="w")
        combo = ctk.CTkComboBox(frame, values=["2025年11月分家賃として", "一部入金残として", "延滞分家賃として", "その他"])
        combo.set("2025年11月分家賃として")
        combo.grid(row=5, column=1, padx=20, pady=15)
        self.entries["家賃内容:"] = combo

        btn = ctk.CTkButton(self, text="PDF発行", command=self.generate, height=60, corner_radius=30, font=("Bold", 22))
        btn.pack(pady=40)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=20)
        self.progress.set(0)

    def generate(self):
        self.progress.start()
        try:
            data = {k.split(":")[0]: v.get() if hasattr(v, 'get') else v.get("0.0", "end").strip() 
                    for k, v in self.entries.items()}
            data["家賃内容"] = self.entries["家賃内容:"].get()

            today = datetime.now().strftime('%Y%m%d')
            count = cursor.execute("SELECT COUNT(*) FROM rent_receipts").fetchone()[0] + 1
            azukari_no = f'AZ-{today}-{count:03d}'
            receipt_no = f'REC-{today}-{count:03d}'

            filename = os.path.join(pdf_dir, f"{receipt_no}.pdf")
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            segment_h = height / 3

            def draw(y, title):
                c.setFont("Helvetica-Bold", 14)
                c.drawCentredString(width/2, y, title)
                c.drawCentredString(width/2, y-30, "家賃受領証")
                c.setFont("Helvetica", 10)
                c.drawString(50, y-60, "株式会社いこい住宅")
                c.drawString(50, y-80, "〒700-0861 岡山県岡山市北区清輝橋３丁目７－２０")
                c.drawString(50, y-100, "TEL:086-233-2202")
                c.drawRightString(width - 50, y-60, f"預り証番号: {azukari_no}")
                c.drawRightString(width - 50, y-80, f"受領証番号: {receipt_no}")
                c.drawString(50, y-130, f"支払人: {data['支払人名']} 様")
                if data["代理人名"]:
                    c.drawString(50, y-150, f"代理人: {data['代理人名']} 様")
                c.drawString(50, y-180, data["家賃内容"])
                c.setFont("Helvetica-Bold", 18)
                c.drawCentredString(width/2, y-220, f"金 {data['受領金額']} 円")
                c.setFont("Helvetica", 10)
                c.drawString(50, y-250, "(非課税)")
                c.drawString(50, y-270, "振込手数料: 弊社負担")
                c.drawString(50, y-300, f"備考: {data['備考']}")
                c.drawRightString(width - 50, y-340, "代表取締役 小林信弘")

            c.drawCentredString(width/2, height - 50, "【こちら側記録スペース（白紙）】")
            c.setDash(6,6)
            c.line(50, segment_h*2, width-50, segment_h*2)
            c.drawCentredString(width/2, segment_h*2 - 20, "--------------- 切り取り線 ---------------")
            draw(segment_h*2 - 80, "【弊社控え】")
            c.line(50, segment_h, width-50, segment_h)
            c.drawCentredString(width/2, segment_h - 20, "--------------- 切り取り線 ---------------")
            draw(segment_h - 80, "【支払人お渡し用】")

            c.showPage()
            c.save()

            cursor.execute("INSERT INTO rent_receipts VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (azukari_no, receipt_no, *data.values()))
            conn.commit()
            webbrowser.open(filename)
        except Exception as e:
            ctk.CTkMessagebox(title="エラー", message=str(e), icon="cancel")
        finally:
            self.progress.stop()

app = App()
app.mainloop()