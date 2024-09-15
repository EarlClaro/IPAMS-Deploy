import React, { Component } from 'react';
import Logo from '../nalcLogo.png';
class HomePage extends Component {
    render() {
        return (
            <div>
                <img src={Logo} className="rounded mx-auto d-block" alt="nalc logo" style={{ height: '400px' }} />
                <h1 style={{textAlign: 'center'}}><strong>Narrative Association for Linked Content</strong> (NALC)</h1>
                <h3 style={{textAlign: 'center'}}>Ask your question below!</h3>
            </div>
        );
    }
}

export default HomePage;