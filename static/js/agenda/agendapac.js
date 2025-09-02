import { Calendar } from '@fullcalendar/core';
import listWeekPlugin from '@fullcalendar/list';

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const eventsJson = document.getElementById('events-data').textContent.trim() || '[]';
    const events = JSON.parse(eventsJson);

    let calendar = new Calendar(calendarEl, {
        plugins: [
            listWeekPlugin
        ],
        initialDate: new Date(),
        selectable: true,
        selectMirror: true,
        editable: false,
        dayMaxEvents: true,
        timeZone: 'local', 
        slotMinTime: '07:00:00',
        slotMaxTime: '18:30:00',
        allDaySlot: false,
        displayEventTime: true,
        events: events.map(event => ({
    id: event.id,
    title: `${event.medico} - ${event.procedimentos}`,
    start: event.start,
    end: event.end,
    extendedProps: {
        avatar: event.avatar,
        paciente: event.paciente,
        medico: event.medico,
        genero: event.genero,
        data_nascimento: event.data_nascimento,
        procedimentos: event.procedimentos,
        convenio: event.convenio,
        observacoes: event.observacoes,
        status: event.status
    },
    backgroundColor: event.status === 'Agendado' ? '#2035ecff' : event.status === 'Confirmado' ? '#34D399' : event.status === 'Cancelado' ? '#F87171' : event.status === 'Concluido' ? '#006b44ff' : '#ffffffff',
    borderColor: event.status === 'Agendado' ? '#2035ecff' : event.status === 'Confirmado' ? '#34D399' : event.status === 'Cancelado' ? '#F87171' : event.status === 'Concluido' ? '#006b44ff' : '#ffffffff',
    textColor: '#FFFFFF',
})),
        initialView: 'listWeek',
        locale: 'pt-br',
        buttonText: {
            today: 'Hoje',
            timeGridWeek: 'Semana',
            timeGridDay: 'Dia',
            allDay: 'Dia Inteiro'
        },
        allDayText: 'Dia Inteiro',
        noEventsContent: 'Nenhum agendamento encontrado.'
    })
    calendar.render()
})