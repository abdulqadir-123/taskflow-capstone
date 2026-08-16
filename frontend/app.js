const API = "http://127.0.0.1:8000";
let currentProject = null;
const $ = id => document.getElementById(id);

async function api(path, options={}) {
  const r = await fetch(API + path, {headers: {"Content-Type":"application/json"}, ...options});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}
function msg(t){$("message").textContent=t}
async function seed(){
  try{
    const d=await api("/seed",{method:"POST"});
    currentProject=d.project_id;
    msg("Demo data loaded");
    await loadAll();
  }catch(e){msg(e.message)}
}
async function loadAll(){
  try{
    const projects=await api("/projects");
    $("projects").textContent=projects.length;
    if(!currentProject && projects.length) currentProject=projects[0].id;
    await loadTasks();
    const s=await api("/statistics"+(currentProject?`?project_id=${currentProject}`:""));
    $("total").textContent=s.total;
    $("done").textContent=s.completed;
    $("progress").textContent=s.completion_percent+"%";
  }catch(e){msg("Start backend first, then click Load demo data")}
}
async function loadTasks(){
  if(!currentProject){$("tasks").innerHTML="<p>No project yet. Click Load demo data.</p>";return}
  const sort=$("sort").value;
  const tasks=await api(`/tasks?project_id=${currentProject}&sort=${sort}`);
  render(tasks);
}
function render(tasks){
  $("tasks").innerHTML=tasks.map(t=>`
    <article class="task">
      <div>
        <h4>${escapeHtml(t.title)}</h4>
        <div class="meta">${escapeHtml(t.description||"")}</div>
        <div style="margin-top:8px">
          <span class="badge ${t.priority}">${t.priority}</span>
          <span class="badge ${t.status}">${t.status}</span>
          ${t.due_date?`<span class="badge">Due ${t.due_date}</span>`:""}
        </div>
      </div>
      <button onclick="deleteTask(${t.id})">Delete</button>
    </article>`).join("");
}
async function deleteTask(id){
  await api(`/tasks/${id}`,{method:"DELETE"});
  await loadAll();
}
let timer;
function searchTasks(){
  clearTimeout(timer);
  timer=setTimeout(async()=>{
    const q=$("search").value.trim();
    if(!q){loadTasks();return}
    const tasks=await api(`/tasks/search?q=${encodeURIComponent(q)}&project_id=${currentProject}`);
    render(tasks);
  },250);
}
async function quickAdd(){
  const text=$("quickText").value.trim();
  if(!text)return;
  if(!currentProject){await seed();return quickAdd()}
  try{
    const task=await api("/quick-add",{method:"POST",body:JSON.stringify({text,project_id:currentProject})});
    $("quickText").value="";
    msg(`Created: ${task.title}`);
    await loadAll();
  }catch(e){msg(e.message)}
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
loadAll();
