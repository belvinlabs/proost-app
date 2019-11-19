import React from 'react';
import Container from '@material-ui/core/Container';
import { fromJS } from 'immutable';
import ConnectionDetails from './ConnectionDetails';


const TEST_ACCOUNT_CONNECTION_DETAILS = fromJS({
  host: 'hackernews.ckfjfiqb1qvb.us-east-2.rds.amazonaws.com',
  port: 3306,
  username: 'proosttestacct_gmail_com',
  password: ']Ll9@PqX/&',
  name: 'proosttestacct_gmail_com'
});


const signinUrl = document.location.hostname === 'localhost'
  ? 'http://localhost:5000/auth/google/init' : '/auth/google/init';

const SignInButton = () => (
    <Container maxWidth="md">
      <div style={{width: '100%', marginTop: '50px',
                   display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <p>
          Welcome to Proost! Proost lets you sync any Google Calendars you can access to your own MySQL database,
          which Proost creates for you. From there, you can do whatever you like using any tool that can connect
          to a MySQL database. As one option, here's
          a <a href="https://colab.research.google.com/drive/18xRMmXcbk2i82A3CvZZOK2_WsKDWPKwf" target="_blank" rel="noopener noreferrer">
          Colab template
          </a> for
          connecting to your Proost database and loading calendar events into a pandas DataFrame.
        </p>
        <p>
          To get started, sign in with Google. Proost requests three permissions:
          <ol>
            <li>
              Read-only access to your profile information, so we can use your real name to improve your experience with Proost
            </li>
            <li>
              Read-only access to Google Calendar, so Proost can sync your events and
              event attendees (a.k.a. guests) to the private MySQL database we create for you
            </li>
            <li>
              Read-only access to your G Suite company directory, <i>solely</i> so Proost can
              provide you with a complete list of calendars that you have the option to sync
            </li>
          </ol>
        </p>
        <a href={signinUrl}>
          <img alt="Google signin" src="/images/google_signin.png" width="250" />
        </a>
        <p>
          By signing into Proost, you agree to
          Proost's <a href="https://www.getproost.com/license-agreement">License Agreement</a> and <a href="https://www.getproost.com/privacy-policy">Privacy Policy</a>.
        </p>
        <p>
          Not ready to sync your own calendars? Play with our public MySQL database,
          which contains events from
          the <a href="https://calendar.google.com/calendar/embed?src=msacpn523mpjgq0jlooh41eme4%40group.calendar.google.com" target="_blank" rel="noopener noreferrer">
          Worldwide Space Launches</a> calendar.
          <ul>
            <li>
              Explore and branch
              off <a href="https://colab.research.google.com/drive/1JmxInvtG1j-4c40mue77Msk7AYYnW9P4#scrollTo=-LayaXSjz1QN" target="_blank" rel="noopener noreferrer">
              this sample Colab project
              </a> showing the launch patterns of various rockets
            </li>
            <li>
              Connection details:
            </li>
          </ul>
          <ConnectionDetails details={TEST_ACCOUNT_CONNECTION_DETAILS} />
        </p>
      </div>
    </Container>
);

export default SignInButton;
