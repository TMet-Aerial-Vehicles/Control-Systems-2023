import { Outlet, Link } from "react-router-dom";
import "./Layout.css"

function Layout() {
    return (
        <>
            <nav>
                <ul>
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/task-1">Task 1</Link>
                    </li>
                    <li>
                        <Link to="/task-2">Task 2</Link>
                    </li>
                </ul>
            </nav>

            <Outlet />
        </>
    )
}

export default Layout
