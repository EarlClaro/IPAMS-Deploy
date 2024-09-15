import React, { Component } from 'react';
import '../Screen/Home/Home.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faRightFromBracket , faUser,  faTrash} from '@fortawesome/free-solid-svg-icons'
import { dotStream } from 'ldrs';

class UserOption extends Component {
    handleProfileClick = () => {
        const { navigate } = this.props;
        navigate('/profile');
    };

    render() {
        const { userData , Logout , DeleteAll } = this.props;
        dotStream.register()

        return (
            <div className="btn-group dropup d-grid gap-2 col-6 mx-auto">
                <button class="btn btn-warning btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                {userData && userData.name ? (
                    userData.name
                ) : (
                    <l-dot-stream size="50" speed="2.5" color="black"></l-dot-stream>
                )}
                </button>
                <ul className="dropdown-menu mx-auto">
                    <li>
                        <a class="dropdown-item" href="#" onClick={this.handleProfileClick}>
                            <FontAwesomeIcon icon={faUser} style={{color: "#541212",}} />
                            {"  "}Profile
                        </a>
                    </li>
                    <li>
                        <a class="dropdown-item" onClick={DeleteAll}>
                            <FontAwesomeIcon icon={faTrash} style={{color: "#541212",}} />
                            {"  "}Delete All Chat
                        </a>
                    </li>
                    <li>
                        <a class="dropdown-item" onClick={Logout}>
                            <FontAwesomeIcon icon={faRightFromBracket} style={{color: "#541212",}} />
                            {"  "}Logout
                        </a>
                    </li>
                </ul>
            </div>
        );
    }
}

export default UserOption;
