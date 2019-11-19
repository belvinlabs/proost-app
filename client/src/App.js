import React from "react";
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import DatabaseDetails from './components/DatabaseDetails';
import Nav from './components/Nav';
import Footer from './components/Footer';
import SignInButton from './components/SignIn';



class App extends React.Component {
  loadTracking() {
    var analytics = window.analytics = window.analytics || [];
    if (!analytics.initialize)
      if (analytics.invoked) window.console && console.error && console.error("Segment snippet included twice.");
      else {
        analytics.invoked = !0;
        analytics.methods = ["trackSubmit", "trackClick", "trackLink", "trackForm", "pageview", "identify", "reset", "group", "track", "ready", "alias", "debug", "page", "once", "off", "on"];
        analytics.factory = function(t) {
          return function() {
            var e = Array.prototype.slice.call(arguments);
            e.unshift(t);
            analytics.push(e);
            return analytics
          }
        };
        for (var t = 0; t < analytics.methods.length; t++) {
          var e = analytics.methods[t];
          analytics[e] = analytics.factory(e)
        }
        analytics.load = function(t, e) {
          var n = document.createElement("script");
          n.type = "text/javascript";
          n.async = !0;
          n.src = "https://cdn.segment.com/analytics.js/v1/" + t + "/analytics.min.js";
          var a = document.getElementsByTagName("script")[0];
          a.parentNode.insertBefore(n, a);
          analytics._loadOptions = e
        };
        analytics.SNIPPET_VERSION = "4.1.0";
        analytics.load("JgeYFd2m50t8V0554cHLRRFTYFOLa9iV");
        analytics.page();
      }
  }

  render() {
    this.loadTracking();

    return (
      <Router>
        <React.Fragment>
          <CssBaseline />
          <Container>
            <Nav />
            <div style={{width: '100%'}}>
              <Switch>
                <Route path="/database">
                  <DatabaseDetails />
                </Route>
                {/* <Route path="/analytics">
                  <Analyses />
                </Route> */}
                <Route path="/">
                  <SignInButton />
                </Route>
              </Switch>
            </div>
          </Container>
          <Footer />
        </React.Fragment>
      </Router>
    );
  }
};

export default App;