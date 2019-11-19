import { createSelector } from 'reselect';
import { Map } from 'immutable';


const availableCalendars = state => state.get('availableCalendars');
const syncedCalendars = state => state.get('syncedCalendars');


export const syncStatusPerCalendar = createSelector(
    availableCalendars,
    syncedCalendars,
    (availableCalendars, syncedCalendars) => availableCalendars.reduce((perCalendar, calendar) => {
      return perCalendar.set(calendar.get('id'), syncedCalendars.includes(calendar.get('id')));
    }, Map())
);


export const syncedCalendarDetails = createSelector(
    availableCalendars,
    syncedCalendars,
    (availableCalendars, syncedCalendars) => availableCalendars.filter(
        (cal) => syncedCalendars.includes(cal.get('id'))
    )
);
