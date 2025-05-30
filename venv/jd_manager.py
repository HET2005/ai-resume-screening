import json
import uuid

JD_FILE = "jd_library.json"

def load_jds():
    try:
        with open("jd_library.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_jds(jds):
    with open(JD_FILE, "w") as f:
        json.dump(jds, f, indent=4)

def add_jd(title, description):
    jds = load_jds()
    new_jd = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description
    }
    jds.append(new_jd)
    save_jds(jds)

def delete_jd(jd_id):
    jds = load_jds()
    jds = [jd for jd in jds if jd["id"] != jd_id]
    save_jds(jds)

def update_jd(jd_id, new_title, new_description):
    jds = load_jds()
    for jd in jds:
        if jd["id"] == jd_id:
            jd["title"] = new_title
            jd["description"] = new_description
            break
    save_jds(jds)
