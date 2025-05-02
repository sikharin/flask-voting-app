import os
from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# ตั้งค่า Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('flask-voting-app-8640e6a3f53c.json', scope)
client = gspread.authorize(creds)

# โหลด Sheet หลัก
score_sheet = client.open("Votes").worksheet("Scores")
project_sheet = client.open("Votes").worksheet("Projects")

# ดึงข้อมูลชื่อผลงาน + รูปจากแผ่น Projects
project_data = project_sheet.get_all_records()
project_lookup = {
    str(row["project_id"]): {
        "title": row["project_title"],
        "image": row["image_url"]
    } for row in project_data
}

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/score', methods=['GET', 'POST'])
def score():
    project_id = request.args.get('project')
    judge_id = request.args.get('judge')

    if not project_id or not judge_id:
        return "Missing project or judge ID"

    if request.method == 'POST':
        creativity = request.form['creativity']
        feasibility = request.form['feasibility']
        presentation = request.form['presentation']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ตรวจว่าลงคะแนนไปแล้วหรือยัง
        data = score_sheet.get_all_records()
        for row in data:
            if str(row['project_id']) == project_id and str(row['judge_id']) == judge_id:
                return render_template("already_voted.html")

        # บันทึกคะแนน
        score_sheet.append_row([timestamp, project_id, judge_id, creativity, feasibility, presentation])
        return render_template("already_voted.html")

    # ส่งข้อมูลแสดงผล
    info = project_lookup.get(str(project_id), {
        "title": f"ผลงาน {project_id}",
        "image": "https://via.placeholder.com/150"
    })

    return render_template('score_form.html',
                           project_id=project_id,
                           judge_id=judge_id,
                           project_title=info["title"],
                           project_image=info["image"])

@app.route('/dashboard')
def dashboard():
    data = score_sheet.get_all_records()
    projects = {}
    for row in data:
        pid = str(row['project_id'])
        if pid not in projects:
            projects[pid] = {'creativity': [], 'feasibility': [], 'presentation': []}
        projects[pid]['creativity'].append(int(row['creativity']))
        projects[pid]['feasibility'].append(int(row['feasibility']))
        projects[pid]['presentation'].append(int(row['presentation']))

    summary = []
    for pid, scores in projects.items():
        creativity = sum(scores['creativity']) / len(scores['creativity'])
        feasibility = sum(scores['feasibility']) / len(scores['feasibility'])
        presentation = sum(scores['presentation']) / len(scores['presentation'])

        info = project_lookup.get(str(pid), {
            "title": f"ผลงาน {pid}",
            "image": "https://via.placeholder.com/150"
        })

        summary.append({
            'project': pid,
            'project_title': info["title"],
            'project_image': info["image"],
            'creativity': creativity,
            'feasibility': feasibility,
            'presentation': presentation,
            'total_score': creativity + feasibility + presentation
        })

    return render_template('dashboard.html', summary=summary)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
