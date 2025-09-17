import {
    Calendar
} from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

function dataFormat(data) {
    const dataJS = new Date(data);
    dataJS.setMinutes(dataJS.getMinutes() - dataJS.getTimezoneOffset());
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
    return d.toLocaleString('pt-br');
}

function formatDateOnly(dataStr) {
    if (!dataStr) return '';
    const d = new Date(dataStr);
    return d.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}
document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const modalCreate = document.getElementById('create_modal');
    const modalView = document.getElementById('view_modal');
    const modalBlock = document.getElementById('block_modal');
    const deleteBtn = document.getElementById('delete-event-button');
    const editBtn = document.getElementById('edit-event-button');
    const startInput = document.getElementById('id_data_inicio');
    const endInput = document.getElementById('id_data_fim');
    const eventsJsonEl = document.getElementById('events-data');
    const eventsJson = eventsJsonEl ? eventsJsonEl.textContent.trim() : '[]';
    let combinedEvents;
    try {
        combinedEvents = JSON.parse(eventsJson);
    } catch (e) {
        console.error("Erro ao parsear eventos JSON: ", e);
        combinedEvents = [];
    }
    let calendar = new Calendar(calendarEl, {
        plugins: [
            dayGridPlugin,
            timeGridPlugin,
            interactionPlugin
        ],
        customButtons: {
            blockButton: {
                text: 'Bloquear Dia',
                click: function () {
                    modalBlock.showModal();
                }
            }
        },
        headerToolbar: {
            left: 'prev,next,today blockButton',
            center: 'title',
            right: 'timeGridWeek,timeGridDay'
        },
        initialDate: new Date(),
        navLinks: true,
        selectable: true,
        selectMirror: true,
        editable: false,
        dayMaxEvents: true,
        timeZone: 'local',
        slotMinTime: '07:00:00',
        slotMaxTime: '18:30:00',
        allDaySlot: false,
        displayEventTime: true,
        events: combinedEvents,
        initialView: 'timeGridWeek',
        locale: 'pt-br',
        nowIndicator: 'true',
        buttonText: {
            today: 'Hoje',
            timeGridWeek: 'Semana',
            timeGridDay: 'Dia',
        },
        eventOverlap: false,
        selectOverlap: function (event) {
            return event.display !== 'background';
        },
        select: function (arg) {
            if (arg.allDay) {
                calendar.unselect();
                return;
            }
            const dayOfWeekSelected = arg.start.getDay();
            const selectionStart = arg.start;
            const selectionEnd = arg.end;
            const blockedEvent = calendar.getEvents().find(event => {
                const props = event.extendedProps;
                return event.display === 'background' && Array.isArray(props.daysOfWeek) && props.daysOfWeek.includes(dayOfWeekSelected);
            });
            if (blockedEvent) {
                const blockedStart = new Date(blockedEvent.extendedProps.horario_inicio);
                const blockedEnd = new Date(blockedEvent.extendedProps.horario_fim);
                if (selectionStart >= blockedStart && selectionEnd <= blockedEnd) {
                    calendar.unselect();
                    alert('Não é possível criar um agendamento neste horário, pois ele está bloqueado.');
                    return;
                }
            }
            if (startInput) startInput.value = arg.startStr.slice(0, 16);
            if (endInput && arg.end) endInput.value = arg.endStr.slice(0, 16);
            modalCreate.showModal();
            calendar.unselect();
        },
        eventClick: function (arg) {
            const e = arg.event;
            const data = e._def.extendedProps;
            const eventId = e.id;
            if (typeof eventId === 'string' && eventId.startsWith('bloqueio-')) {
                return;
            }
            const avatarEl = document.getElementById('paciente_avatar');
            if (avatarEl) {
                if (data.avatar) {
                    avatarEl.innerHTML = `<img src="${data.avatar}" alt="Avatar" style="width: 80px; height: 80px; border-radius: 50%;">`;
                } else {
                    avatarEl.innerHTML = '';
                }
            }
            document.getElementById('paciente_nome').textContent = data.paciente || '';
            document.getElementById('paciente_genero').textContent = data.genero || '';
            document.getElementById('paciente_data_nascimento').textContent = formatDateOnly(data.data_nascimento) || '';
            document.getElementById('procedimentos_detalhes').textContent = data.procedimentos || '';
            document.getElementById('observacoes_detalhes').textContent = data.observacoes || '';
            document.getElementById('status_detalhes').textContent = data.status || '';
            document.getElementById('data_inicio_detalhes').textContent = formatDateTime(e.start) || '';
            document.getElementById('data_fim_detalhes').textContent = formatDateTime(e.end) || '';
            deleteBtn.setAttribute("data-event-id", eventId);
            editBtn.setAttribute("href", `/dashboard/administradores/agendamentos/editar/${eventId}`);
            modalView.showModal();
        },
    });
    calendar.render();
    deleteBtn.addEventListener('click', function () {
        const eventId = this.getAttribute('data-event-id');
        if (!eventId) return;
        if (confirm('Tem certeza que deseja deletar este evento?')) {
            fetch(`/dashboard/administradores/agendamentos/deletar/${eventId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }  
            })
            location.reload()
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao deletar o evento.');
                }
                return response.json();
            }).then(data => {
                alert(data.message);
                modalView.close();
                const event = calendar.getEventById(eventId);
                if (event) event.remove();
            }).catch(() => alert('Erro ao deletar evento.'));
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