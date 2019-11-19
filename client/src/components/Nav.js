import React from 'react';
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import Container from '@material-ui/core/Container';
import {connect} from 'react-redux';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

const TABS = [
  // {
  //   label: 'Database',
  //   path: '/database'
  // },
  {
    label: 'Analytics',
    path: '/analytics'
  }
];


const mapStateToProps = (state) => ({
  userInfo: state.get('userInfo')
});


class Nav extends React.Component {
  static propTypes = {
    history: PropTypes.object.isRequired
  };

  constructor(props) {
    super(props);

    this.state = {
      currentPath: document.location.pathname.trim()
    };
  }

  componentWillMount = () => {
    this.props.history.listen((location, action) => {
      this.setState({currentPath: location.pathname.trim()});
    });
  };

  componentDidUpdate = () => {
    if (this.state.currentPath.length > 1 && this.props.userInfo === null) {
      this.handleChange(null, '/');
    }
  };

  handleChange = (event, newValue) => {
    this.setState({ currentPath: newValue });
    this.props.history.push(newValue);
    window.analytics.page();
  };

  render() {
    if (this.state.currentPath.length <= 1) return null;

    return (
      <Container maxWidth="md">
        <Tabs
          value={this.state.currentPath}
          onChange={this.handleChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
          centered
        >
          {TABS.map(tab => <Tab key={tab.path} label={tab.label} value={tab.path} />)}
        </Tabs>
      </Container>
    );
  }
}

export default connect(
    mapStateToProps,
    {}
)(withRouter(Nav));
