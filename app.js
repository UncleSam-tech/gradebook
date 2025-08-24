// public/app.js
const LS_KEY = "grades"; // { student: { subject: [grades...] } }
const API_BASE = "/api/index"; // because file is api/index.py

const $ = (id) => document.getElementById(id);
const state = { grades: {} };

function load() {
  try {
    state.grades = JSON.parse(localStorage.getItem(LS_KEY) || "{}");
  } catch {
    state.grades = {};
  }
}

function save() {
  localStorage.setItem(LS_KEY, JSON.stringify(state.grades));
  render();
}

function ensureStudent(name) {
  if (!state.grades[name]) state.grades[name] = {};
}

function ensureSubject(student, subject) {
  ensureStudent(student);
  if (!state.grades[student][subject]) state.grades[student][subject] = [];
}

function render() {
  // Students list
  const ul = $("studentsList");
  ul.innerHTML = "";
  Object.keys(state.grades).forEach((s) => {
    const li = document.createElement("li");
    li.textContent = s;
    ul.appendChild(li);
  });

  // Rebuild selects
  const selects = [$("studentSelect"), $("avgStudent"), $("avgStudent2")];
  selects.forEach((sel) => (sel.innerHTML = ""));
  Object.keys(state.grades).forEach((s) => {
    selects.forEach((sel) => {
      const opt = document.createElement("option");
      opt.value = s;
      opt.textContent = s;
      sel.appendChild(opt);
    });
  });

  rebuildSubjectSelect();

  // Table
  const tbody = $("dataTable").querySelector("tbody");
  tbody.innerHTML = "";
  for (const [student, subjects] of Object.entries(state.grades)) {
    const subjectNames = Object.keys(subjects);
    if (subjectNames.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${student}</td><td class="muted">—</td><td class="muted">—</td>`;
      tbody.appendChild(tr);
    } else {
      for (const subj of subjectNames) {
        const tr = document.createElement("tr");
        const grades = subjects[subj].join(", ");
        tr.innerHTML = `<td>${student}</td><td>${subj}</td><td>${grades || "<span class='muted'>none</span>"}</td>`;
        tbody.appendChild(tr);
      }
    }
  }
}

function rebuildSubjectSelect() {
  const student = $("studentSelect").value || Object.keys(state.grades)[0];
  const subjectSel = $("subjectSelect");
  subjectSel.innerHTML = "";
  if (!student || !state.grades[student]) return;
  const subjects = Object.keys(state.grades[student]);
  subjects.forEach((subj) => {
    const opt = document.createElement("option");
    opt.value = subj;
    opt.textContent = subj;
    subjectSel.appendChild(opt);
  });
}

/* ---------- UI handlers ---------- */
$("addStudent").onclick = () => {
  const name = $("studentName").value.trim();
  if (!name) return alert("Enter a student name.");
  ensureStudent(name);
  $("studentName").value = "";

  // Select the newly added student in all dropdowns
  ["studentSelect", "avgStudent", "avgStudent2"].forEach((id) => {
    const sel = $(id);
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = name;
    sel.appendChild(opt);
    sel.value = name;
  });

  save();
};

$("addSubject").onclick = () => {
  const student = $("studentSelect").value || $("studentName").value.trim();
  const subject = $("subjectName").value.trim();
  if (!student) return alert("Pick/create a student first.");
  if (!subject) return alert("Enter a subject name.");
  ensureSubject(student, subject);
  $("subjectName").value = "";

  // Reflect new subject in subjectSelect and select it
  rebuildSubjectSelect();
  $("subjectSelect").value = subject;

  save();
};

$("studentSelect").onchange = rebuildSubjectSelect;

$("addGrade").onclick = () => {
  const student = $("studentSelect").value;
  const subject = $("subjectSelect").value || $("subjectName").value.trim();
  const raw = $("gradeVal").value.trim();
  const v = Number(raw);
  if (!student) return alert("Pick a student.");
  if (!subject) return alert("Pick or create a subject.");
  if (!Number.isFinite(v) || v < 0 || v > 100) return alert("Grade must be 0–100.");
  ensureSubject(student, subject);
  state.grades[student][subject].push(v);
  $("gradeVal").value = "";
  save();
};

$("clearAll").onclick = () => {
  if (confirm("Clear all data?")) {
    state.grades = {};
    save();
  }
};

/* ---------- API helpers ---------- */
async function post(path, payload) {
  const url = `${API_BASE}${path}`; // ensure /api/index prefix
  try {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!r.ok) {
      // try to capture text body for easier debugging
      const txt = await r.text().catch(() => "");
      throw new Error(`HTTP ${r.status} ${r.statusText}${txt ? ` - ${txt}` : ""}`);
    }

    return await r.json();
  } catch (error) {
    console.error("API Error:", error);
    return { error: error.message || "Network error occurred" };
  }
}

/* ---------- Reports ---------- */
$("btnStudentAvg").onclick = async () => {
  const student = $("avgStudent").value;
  if (!student) return alert("Please select a student.");
  const data = await post("/student-avg", { grades: state.grades, student });
  $("out").textContent = JSON.stringify(data, null, 2);
};

$("btnSubjectAvg").onclick = async () => {
  const student = $("avgStudent2").value;
  const subject = $("avgSubject").value.trim();
  if (!student) return alert("Please select a student.");
  if (!subject) return alert("Enter subject name.");
  const data = await post("/subject-avg", { grades: state.grades, student, subject });
  $("out").textContent = JSON.stringify(data, null, 2);
};

$("btnRank").onclick = async () => {
  if (Object.keys(state.grades).length === 0) return alert("Add some students and grades first.");
  const data = await post("/students-rank", { grades: state.grades });
  $("out").textContent = JSON.stringify(data, null, 2);
};

$("btnFullReport").onclick = async () => {
  const student = $("avgStudent").value || Object.keys(state.grades)[0] || "";
  if (!student) return alert("Add a student first.");
  const data = await post("/full-student-data", { grades: state.grades, student });
  $("out").textContent = JSON.stringify(data, null, 2);
};

/* ---------- init ---------- */
load();
render();

// quick health check on load (optional)
fetch(`${API_BASE}/ping`).then(r => {
  if (!r.ok) throw new Error("Ping failed");
  return r.json();
}).then(j => console.log("API ping:", j))
  .catch(e => console.warn("API ping error:", e.message));
