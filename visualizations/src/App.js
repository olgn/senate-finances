import React from 'react'
import Network from './components/features/network/Network'
import SQLiteContextProvider from './components/wrappers/SQLiteContext'

function App() {
    return (
        <div className="App">
            <SQLiteContextProvider>
                <Network />
            </SQLiteContextProvider>
        </div>
    )
}

export default App
