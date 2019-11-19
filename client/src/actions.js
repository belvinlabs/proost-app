const axios = require('axios');


const receiveUserInfo = (user) => ({
  type: 'SET_USER_INFO',
  user
});


export const fetchUserInfo = () => (dispatch, getState) => {
  axios.get('/api/users/me')
    .then(function (response) {
      dispatch(receiveUserInfo(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
};


const receiveAvailableCalendars = (calendars) => ({
  type: 'SET_AVAILABLE_CALENDARS',
  calendars
});


export const fetchAvailableCalendars = () => (dispatch, getState) => {
  axios.get('/api/calendars')
    .then(function (response) {
      dispatch(receiveAvailableCalendars(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
};


export const selectCalendar = (calendarId, selected) => ({
  type: 'SELECT_CALENDAR',
  calendarId,
  selected
});


export const updateSyncSettings = () => (dispatch, getState) => {
  window.fbq('track', 'CompleteRegistration');

  axios.post('/api/settings/mine', {
      synced_calendars: getState().get('syncedCalendars').toArray()
    })
    .then(function (response) {
      dispatch(receiveSyncConfig(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
};


const receiveSyncConfig = (syncConfig) => ({
  type: 'UPDATE_SYNC_SETTINGS',
  syncConfig
});


export const fetchSyncConfig = () => (dispatch, getState) => {
  axios.get('/api/settings/mine')
    .then(function (response) {
      if (!response.data) return;

      dispatch(receiveSyncConfig(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
};


const receiveDatabaseDetails = (databaseDetails) => ({
  type: 'SET_DATABASE_DETAILS',
  databaseDetails
});


export const fetchDatabaseDetails = () => (dispatch, getState) => {
  axios.get('/api/databases/mine')
    .then(function (response) {
      if (!response.data) return;

      dispatch(receiveDatabaseDetails(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
};
