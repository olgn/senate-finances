import React, { createContext, useContext, useEffect, useState } from 'react'

import { SQLiteContext } from '../../../wrappers/SQLiteContext'
import { resultsToData, resultsToColumnData } from '../../../../utils/sqlite'

const DataContext = createContext(null)

export default ({ children }) => {
    const { db } = useContext(SQLiteContext)
    const [columns, setColumns] = useState([])
    const [data, setData] = useState([])

    useEffect(() => {
        if (db) {
            const results = db.exec('SELECT * FROM senators')
            setColumns(resultsToColumnData(results))
            setData(resultsToData(results))
        }
    }, [db])

    return (
        <DataContext.Provider value={{ columns, data }}>
            {children}
        </DataContext.Provider>
    )
}

export { DataContext }