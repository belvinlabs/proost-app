import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';


import {connect} from 'react-redux';
import * as actions from '../../actions';
import { syncedCalendarDetails } from '../../getters';


const mapStateToProps = (state) => ({
  syncedCalendarDetails: syncedCalendarDetails(state)
});




class Analytics extends React.Component {
  render() {
    return (
        <React.Fragment>
          <CssBaseline />
          <Container maxWidth="md">
            <div style={{height: '20px'}}></div>
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
          </Container>
        </React.Fragment>
    );
  }
}


export default connect(
    mapStateToProps,
    actions
)(Analytics)
