import React from 'react';
import {connect} from 'react-redux';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import * as actions from '../actions';
import { syncStatusPerCalendar } from '../getters';
import ConnectionDetails from './ConnectionDetails';


const mapStateToProps = (state) => ({
  userEmail: state.getIn(['userInfo', 'email']),
  availableCalendars: state.get('availableCalendars'),
  syncedCalendars: state.get('syncedCalendars'),
  syncStatusPerCalendar: syncStatusPerCalendar(state),
  connectionDetails: state.get('databaseDetails')
});


const SyncStarted = () => {
  return  (
              <div>
                <p>
                  Proost has started syncing your calendar data to your very own MySQL database. Proost
                  initially syncs events from 30 days in the past and 30 days in the future, and the
                  sync will take about 30 seconds per calendar.
                </p>
                <p>
                  While we're working hard to add more analytics directly into Proost,
                  we also want you to be able to run any analysis you like as easily as
                  possible. To that end, we've already added you to
                  a <a href="https://www.metabase.com" target="_blank" rel="noopener noreferrer">Metabase</a> instance
                  we manage for you. You can use Metabase to:
                </p>
                <ul>
                  <li>
                    Create charts and dashboards using pure SQL
                  </li>
                  <li>
                    Create charts and dashboards using a point-and-click interface (no SQL required)
                  </li>
                  <li>
                    Examine the schema of the MySQL database we created for you
                  </li>
                </ul>
                <p>
                  To start using Metabase with your calendar data, head to <a href="https://bi.getproost.com">bi.getproost.com</a>. You're already signed in! &#x1f680;
                </p>
              </div>
  )
};


class CalendarsSelector extends React.Component {
  constructor(props) {
    super(props);

    this.state = { syncing: false };
  }

  componentDidMount() {
    if (this.props.syncedCalendars.size === 0) {
      this.selectAll(true);
    }
  }

  selectAll = (select) => {
    this.props.availableCalendars.forEach(cal => this.props.selectCalendar(cal.get('id'), select));
  };

  handleChange = calendarId => event => {
    this.props.selectCalendar(calendarId, event.target.checked);
  };

  handleSubmit = () => {
    this.props.updateSyncSettings();

    this.setState({ syncing: true });
  };

  bulkSelect = () => {
    const noneSelected = this.props.syncedCalendars.size === 0;

    if (noneSelected) {
      this.selectAll(true);
    } else {
      this.selectAll(false);
    }
  };

  render() {
    const sortedCalendars = this.props.availableCalendars.sort(
      (cal1, cal2) => cal1.get('id') === this.props.userEmail ? -1 : 0
    );

    const noneSelected = this.props.syncedCalendars.size === 0;
    const allSelected = this.props.availableCalendars.size === this.props.syncedCalendars.size;

    return (
        <div>
          <h4>
            Calendars to sync
          </h4>
          <FormControl component="fieldset">
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={!noneSelected}
                    onChange={this.bulkSelect}
                    color="secondary"
                    indeterminate={!noneSelected && !allSelected}
                  />
                }
                label=""
              />
              {sortedCalendars.map(calendar => {
                const calendarId = calendar.get('id');

                return (
                    <FormControlLabel
                      key={calendarId}
                      control={<Checkbox checked={this.props.syncStatusPerCalendar.get(calendarId)} color="primary" onChange={this.handleChange(calendarId)} value={calendarId} />}
                      label={calendar.get('summary')}
                    />
                )
              })}
            </FormGroup>
            <Button
                variant="contained"
                color="primary"
                style={{marginTop: '5px'}}
                onClick={this.handleSubmit}
            >
              Start sync
            </Button>
          </FormControl>
          <div style={{marginTop: '20px'}} />
          {
            !this.state.syncing ? null :
            <SyncStarted />
          }
        </div>
    );
  }
}

const CalendarsSelectorContainer = connect(
    mapStateToProps,
    actions
)(CalendarsSelector);


class DatabaseDetails extends React.Component {
  render() {
    if (!this.props.userEmail) return null;

    return (
        <React.Fragment>
          <CssBaseline />
          <Container maxWidth="md">
            <div style={{height: '20px'}}></div>
            <p>
              You are signed in as <b>{this.props.userEmail}</b>.
            </p>
            {this.props.availableCalendars.size === 0 ? null :
                <CalendarsSelectorContainer />
            }
            <br />
            <ConnectionDetails
              details={this.props.connectionDetails}
              hideHeader={true}
            />
          </Container>
        </React.Fragment>
    );
  }
}

export default connect(
    mapStateToProps,
    actions
)(DatabaseDetails);
