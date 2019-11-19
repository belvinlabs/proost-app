import React from 'react';
import Container from '@material-ui/core/Container';


class Footer extends React.Component {
  render() {
    return (
      <div style={{width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', bottom: 0}}>
        <Container maxWidth="md" justify="center" style={{  }}>
          <p>
            We <span role="img" aria-label="love love LOVE">&#10084;&#65039; &#10084;&#65039; &#10084;&#65039;</span> feedback and feature requests. Email us at <a href="mailto:help@getproost.com">help@getproost.com</a>, or add requests <a href="https://trello.com/invite/b/KR2vqVGw/9154fa50b4f3800263fac8e4f133af4b/proost-product-requests" target="_blank" rel="noopener noreferrer">here</a>.
          </p>
        </Container>
      </div>
    );
  }
}

export default Footer;
