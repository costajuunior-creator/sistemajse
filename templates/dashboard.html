{% extends "base.html" %}
{% block content %}
<div class="grid">
  <div class="card">
    <div class="h1" style="font-size:22px;">Nova tarefa</div>
    <p class="p">Adicione uma tarefa rápida e mantenha tudo organizado.</p>

    <form method="post">
      <label>Tarefa</label>
      <input name="title" placeholder="Ex: Estudar 30 min" required>
      <button class="btn" type="submit">Adicionar</button>
    </form>
  </div>

  <div class="card">
    <div class="h1" style="font-size:22px;">Resumo</div>
    <p class="p">Você está logado como <strong>{{ current_user.email }}</strong>.</p>
    <div class="row" style="margin-top:10px;">
      <div class="btn-ghost" style="flex:1; text-align:center;">Pendentes: {{ pending|length }}</div>
      <div class="btn-ghost" style="flex:1; text-align:center;">Concluídas: {{ done|length }}</div>
    </div>
  </div>
</div>

<div class="grid" style="margin-top:16px;">
  <div class="card">
    <div class="h1" style="font-size:20px;">Pendentes</div>
    <p class="p">Clique em “Concluir” quando terminar.</p>

    {% for t in pending %}
      <div class="task">
        <div>
          <div class="title">{{ t.title }}</div>
          <div class="meta">Criada em {{ t.created_at.strftime("%d/%m/%Y %H:%M") }}</div>
        </div>
        <div style="display:flex; gap:8px;">
          <form method="post" action="{{ url_for('toggle_task', task_id=t.id) }}">
            <button class="btn-ghost" type="submit">Concluir</button>
          </form>
          <form method="post" action="{{ url_for('delete_task', task_id=t.id) }}">
            <button class="btn-danger" type="submit">Excluir</button>
          </form>
        </div>
      </div>
    {% else %}
      <p class="p">Nenhuma tarefa pendente ✅</p>
    {% endfor %}
  </div>

  <div class="card">
    <div class="h1" style="font-size:20px;">Concluídas</div>
    <p class="p">Você pode “Reabrir” se precisar.</p>

    {% for t in done %}
      <div class="task done">
        <div>
          <div class="title">{{ t.title }}</div>
          <div class="meta">Criada em {{ t.created_at.strftime("%d/%m/%Y %H:%M") }}</div>
        </div>
        <div style="display:flex; gap:8px;">
          <form method="post" action="{{ url_for('toggle_task', task_id=t.id) }}">
            <button class="btn-ghost" type="submit">Reabrir</button>
          </form>
          <form method="post" action="{{ url_for('delete_task', task_id=t.id) }}">
            <button class="btn-danger" type="submit">Excluir</button>
          </form>
        </div>
      </div>
    {% else %}
      <p class="p">Nenhuma tarefa concluída ainda.</p>
    {% endfor %}
  </div>
</div>

<div class="grid" style="margin-top:16px;">
  <div class="card">
    <div class="h1" style="font-size:20px;">Gráficos</div>
    <p class="p">Visão rápida das tarefas nos últimos 7 dias.</p>
    <div style="height:260px;">
      <canvas id="tasksChart"></canvas>
    </div>
  </div>

  <div class="card">
    <div class="h1" style="font-size:20px;">Calendário</div>
    <p class="p">Suas tarefas aparecem no dia em que foram criadas.</p>
    <div id="calendar" class="calendar"></div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js"></script>

<script>
  const stats = {{ stats|tojson }};
  const ctx = document.getElementById('tasksChart');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: stats.labels,
      datasets: [
        { label: 'Criadas', data: stats.created, tension: 0.35 },
        { label: 'Concluídas', data: stats.completed, tension: 0.35 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#e5e7eb' } } },
      scales: {
        x: { ticks: { color: '#a8b0c0' }, grid: { color: 'rgba(255,255,255,.08)' } },
        y: { ticks: { color: '#a8b0c0' }, grid: { color: 'rgba(255,255,255,.08)' } }
      }
    }
  });

  const events = {{ events|tojson }};
  document.addEventListener('DOMContentLoaded', function() {
    const el = document.getElementById('calendar');
    const cal = new FullCalendar.Calendar(el, {
      initialView: 'dayGridMonth',
      height: 380,
      headerToolbar: { left: 'prev,next today', center: 'title', right: '' },
      events: events
    });
    cal.render();
  });
</script>
{% endblock %}
