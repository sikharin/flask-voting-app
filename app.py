import os
from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

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
        lean_alignment = request.form['lean_alignment']
        process_system = request.form['process_system']
        kpi_and_results = request.form['kpi_and_results']
        knowledge_transfer = request.form['knowledge_transfer']
        creativity_and_engagement = request.form['creativity_and_engagement']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ตรวจว่าลงคะแนนไปแล้วหรือยัง
        data = score_sheet.get_all_records()
        for row in data:
            if str(row['project_id']) == project_id and str(row['judge_id']) == judge_id:
                return render_template("already_voted.html")

        # บันทึกคะแนน
        score_sheet.append_row([timestamp, project_id, judge_id, lean_alignment,process_system,kpi_and_results,knowledge_transfer,creativity_and_engagement])
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
            projects[pid] = {
                'lean_alignment': [],
                'process_system': [],
                'kpi_and_results': [],
                'knowledge_transfer': [],
                'creativity_and_engagement': []
            }

        projects[pid]['lean_alignment'].append(int(row['lean_alignment']))
        projects[pid]['process_system'].append(int(row['process_system']))
        projects[pid]['kpi_and_results'].append(int(row['kpi_and_results']))
        projects[pid]['knowledge_transfer'].append(int(row['knowledge_transfer']))
        projects[pid]['creativity_and_engagement'].append(int(row['creativity_and_engagement']))

    summary = []
    for pid, scores in projects.items():
        lean_alignment = sum(scores['lean_alignment']) / len(scores['lean_alignment']) * 4
        process_system = sum(scores['process_system']) / len(scores['process_system']) * 4
        kpi_and_results = sum(scores['kpi_and_results']) / len(scores['kpi_and_results']) * 4
        knowledge_transfer = sum(scores['knowledge_transfer']) / len(scores['knowledge_transfer']) * 4
        creativity_and_engagement = sum(scores['creativity_and_engagement']) / len(scores['creativity_and_engagement']) * 4

        total_score = lean_alignment + process_system + kpi_and_results + knowledge_transfer + creativity_and_engagement

        info = project_lookup.get(str(pid), {
            "title": f"ผลงาน {pid}",
            "image": "https://via.placeholder.com/150"
        })

        summary.append({
            'project': pid,
            'project_title': info["title"],
            'project_image': info["image"],
            'lean_alignment': round(lean_alignment, 2),
            'process_system': round(process_system, 2),
            'kpi_and_results': round(kpi_and_results, 2),
            'knowledge_transfer': round(knowledge_transfer, 2),
            'creativity_and_engagement': round(creativity_and_engagement, 2),
            'total_score': round(total_score, 2)
        })

    return render_template('dashboard.html', summary=summary)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
