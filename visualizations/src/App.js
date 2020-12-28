import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import SenatorList from './components/features/senators/list/List'
import SenatorDetail from './components/features/senators/detail/Detail'
import SQLiteContextProvider from './components/wrappers/SQLiteContext'
import urls from './utils/constants/urls'

function App() {
    return (
        <div className="App">
            <SQLiteContextProvider>
                <Router>
                    <Switch>
                        <Route exact path={urls.senators}>
                            <SenatorList />
                        </Route>
                        <Route exact path={urls.senatorDetail}>
                            <SenatorDetail />
                        </Route>
                    </Switch>
                </Router>
            </SQLiteContextProvider>
        </div>
    )
}

export default App
