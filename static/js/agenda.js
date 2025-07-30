function dataFormat(data) {
    const dataJS = new Date(data);
    const year = dataJS.getFullYear();
    const month = (dataJS.getMonth() + 1).toString().padStart(2, '0');
    const day = dataJS.getDate().toString().padStart(2, '0');
    const hour = dataJS.getHours().toString().padStart(2, '0');
    const minute = dataJS.getMinutes().toString().padStart(2, '0');
    const second = dataJS.getSeconds().toString().padStart(2, '0');
    return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

function formatDateTime(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleString('pt-BR');
}

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const modalCreate = document.getElementById('create_modal');
    const modalView = document.getElementById('view_modal');
    const deleteBtn = document.getElementById('delete-event-button');
    const editBtn = document.getElementById('edit-event-button');

    const startInput = document.getElementById('id_data_inicio');
    const endInput = document.getElementById('id_data_fim');

    const eventsJson = document.getElementById('events-data').textContent || '[]';
    const events = JSON.parse(eventsJson);

    let calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridWeek,timeGridDay'
        },
        initialDate: new Date(),
        navLinks: true,
        selectable: true,
        selectMirror: true,
        editable: false,
        dayMaxEvents: true,
        events: events,
        initialView: 'timeGridWeek',
        locale: 'pt-br',
        buttonText: {
            today: 'Hoje',
            timeGridWeek: 'Semana',
            timeGridDay: 'Dia',
            allDay: 'Dia Inteiro'
        },
        allDayText: 'Dia Inteiro',


        select: function (arg) {
            if (startInput) startInput.value = arg.startStr.slice(0,16);
            if (endInput && arg.end) endInput.value = arg.endStr.slice(0,16);
            modalCreate.showModal();
            calendar.unselect();
        },

        eventClick: function (arg) {
            const e = arg.event;
            const data = e.extendedProps;

            document.getElementById('procedimentos_detalhes').textContent = data.procedimentos
            document.getElementById('paciente_detalhes').textContent = data.paciente;
            document.getElementById('observacoes_detalhes').textContent = data.observacoes;
            document.getElementById('data_inicio_detalhes').textContent = formatDateTime(e.start);
            document.getElementById('data_fim_detalhes').textContent = formatDateTime(e.end);


            deleteBtn.setAttribute("data-event-id", e.id);
            editBtn.setAttribute("href", `/dashboard/agendamento/edit/${e.id}/`);

            modalView.showModal();
        },
    });

    calendar.render();

    deleteBtn.addEventListener('click', function () {
        const eventId = this.getAttribute('data-event-id');
        if (!eventId) return;

        if (confirm('Tem certeza que deseja deletar este evento?')) {
            fetch(`/dashboard/administrador/agendamentos/deletar/${eventId}`, {
              method: 'POST',
              headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
              })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                modalView.close();
                const event = calendar.getEventById(eventId);
                if (event) event.remove();
            })
            .catch(() => alert('Erro ao deletar evento.'));
        }
    });

    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const parts = cookie.trim().split('=');
            if (parts[0] === name) return decodeURIComponent(parts[1]);
        }
        return null;
    }
});