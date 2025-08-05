// Handle AJAX for API calls
function updateTask(id, status) {
  fetch(`/api/tasks/${id}`, {
    method: 'PUT',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({status:status})
  }).then(()=>location.reload());
}
function deleteTask(id) {
  fetch(`/api/tasks/${id}`, {method:'DELETE'}).then(()=>location.reload());
}
// Override form submission to JSON POST
const form = document.getElementById('add-task-form');
form.addEventListener('submit', e=>{
  e.preventDefault();
  const data = {
    what_to_do: form.what_to_do.value,
    due_date: form.due_date.value
  };
  fetch('/api/tasks', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify(data)
  }).then(()=>location.reload());
});