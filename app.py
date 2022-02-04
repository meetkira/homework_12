from flask import Flask, render_template, request
import json

with open('jsons/candidates.json', encoding='utf-8') as f:
    candidates = json.load(f)

with open('jsons/settings.json') as f:
    settings = json.load(f)

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('index.html', online=settings["online"])


@app.route('/candidate/<int:id>/')
def candidate_page(id):
    return render_template('candidate.html', candidate=candidates[id - 1])


@app.route('/list/')
def list_page():
    return render_template('list.html', candidates=candidates)


@app.route('/search/')
def search_page():
    search = request.args.get('name')
    if not search:
        return "Введите параметр name"

    if settings["case-sensitive"]:
        candidates_search = [candidate for candidate in candidates if search in candidate["name"]]
    else:
        candidates_search = [candidate for candidate in candidates if search.lower() in candidate["name"].lower()]

    candidates_search_len = len(candidates_search)
    return render_template('search.html', candidates=candidates_search, num_of_candidates=candidates_search_len)


@app.route('/skill/<search_skill>')
def skill_page(search_skill):
    candidates_search = []
    for candidate in candidates:
        candidate_skills = candidate["skills"].split(', ')
        if settings["case-sensitive"] == False:
            search_skill = search_skill.lower()
            candidate_skills = [skill.lower() for skill in candidate_skills]
        if search_skill in candidate_skills and len(candidates_search) < settings["limit"]:
            candidates_search.append(candidate)

    candidates_search_len = len(candidates_search)

    return render_template('skill.html', skill=search_skill, candidates=candidates_search,
                           num_of_candidates=candidates_search_len)


if __name__ == "__main__":
    app.run(debug=True)
