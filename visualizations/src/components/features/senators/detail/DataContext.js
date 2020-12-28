import React, { createContext, useContext, useEffect, useState } from 'react'

import { SQLiteContext } from '../../../wrappers/SQLiteContext'
import { resultsToData, resultsToColumnData } from '../../../../utils/sqlite'
import { useParams } from 'react-router-dom'

const DataContext = createContext(null)

export default ({ children }) => {
    const { db } = useContext(SQLiteContext)
    const [columns, setColumns] = useState([])
    const [data, setData] = useState([])
    const [ detailData, setDetailData ] = useState({})
    const { id } = useParams()

    useEffect(() => {
        if (db && id) {
            const results = db.exec(`SELECT * FROM transactions WHERE senator_id = ${id}`)
            setColumns(resultsToColumnData(results))
            setData(resultsToData(results))
        }
    }, [db, id])

    useEffect(() => {
        if (db && id) {
            const stmt = db.prepare('SELECT * FROM senators WHERE id = $id')
            const detailResult = stmt.getAsObject({$id: id})
            setDetailData(detailResult)
        }
    }, [db, id])

    return (
        <DataContext.Provider value={{ columns, data, detailData }}>
            {children}
        </DataContext.Provider>
    )
}

export { DataContext }