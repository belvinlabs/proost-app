import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';
import ReactTooltip from 'react-tooltip';


class Cleartext extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      justCopied: false
    };
  }

  copy = () => {
    const { text } = this.props;

    navigator.clipboard.writeText(text);

    this.setState({justCopied: true});

    window.setTimeout(this.setState.bind(this, {justCopied: false}), 2000);
  };

  render() {
    const { text } = this.props;
    const { justCopied } = this.state;
    let dataTip = !justCopied ? 'Click to copy' : 'Copied!';
    if (!this.props.clickToCopy) {
      dataTip = null;
    }

    return (
        <span
          key={justCopied ? 'copied' : 'copy' /* (forces re-render of tooltip) */}
          data-tip={dataTip}
          style={{cursor: 'pointer'}}
          onClick={this.props.clickToCopy ? this.copy : () => {}}
        >
          {text}
          <ReactTooltip effect="solid" />
        </span>
    )
  }
}


class PasswordCell extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showPassword: false,
    };
  }

  togglePassword = () => {
    this.setState({ showPassword: !this.state.showPassword });
  };

  render() {
    const { password } = this.props;
    const { showPassword } = this.state;

    return (
        <TableCell
            align="right"
            style={{display: 'flex', alignItems: 'center', 'fontFamily': '"Courier New", Courier, monospace'}}
        >
          {showPassword ?
              <VisibilityOff
                style={{marginLeft: '5px', cursor: 'pointer'}}
                onClick={this.togglePassword}
              />
              : <Visibility
                  style={{marginLeft: '5px', cursor: 'pointer'}}
                  onClick={this.togglePassword}
                />
          }
          {!showPassword ? <span>************</span> :
            <Cleartext text={password} clickToCopy={true} />
          }
        </TableCell>
    )
  }
}


const ConnectionDetails = ({ details, hideHeader }) => {
  if (!details) return null;

  const rows = [
    {
      label: 'Host',
      value: details.get('host'),
      clickToCopy: true
    },
    {
      label: 'Port',
      value: details.get('port'),
      clickToCopy: true
    },
    {
      label: 'Username',
      value: details.get('username'),
      clickToCopy: true
    },
    {
      label: 'Password',
      value: details.get('password'),
      clickToCopy: true
    },
    {
      label: 'Database name',
      value: details.get('name'),
      clickToCopy: true
    },
    {
      label: 'Certificate Authority file for SSL',
      value: (
        <a href="https://s3.amazonaws.com/rds-downloads/rds-ca-2015-root.pem" target="_blank" rel="noopener noreferrer">
          Download here
        </a>
      ),
      clickToCopy: false
    }
  ];

  return (
      <div>
        {!hideHeader ? null :
          <h4>
            MySQL connection details
          </h4>
        }
        <Table aria-label="simple table">
          <TableBody>
            {rows.map(row => (
                <TableRow key={row.label}>
                  <TableCell component="th" scope="row">
                    {row.label}
                  </TableCell>
                      {row.label !== 'Password' ?
                      <TableCell align="right" style={{'fontFamily': '"Courier New", Courier, monospace'}}>

                            <Cleartext text={row.value} clickToCopy={row.clickToCopy} />
                      </TableCell>
                      : <PasswordCell password={row.value}/>
                      }
                </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
  );
};


export default ConnectionDetails;
