import React, { useContext, useEffect, useState } from 'react'

import { SQLiteContext } from '../../wrappers/SQLiteContext'
import Table from '../../elem/table/Table'
import { resultsToColumnData, resultsToData } from '../../../utils/sqlite'

const Network = () => {
    const { db } = useContext(SQLiteContext)
    const [results, setResults] = useState([])

    useEffect(() => {
        if (db) {
            // const results = db.exec("SELECT `name`, `sql`\n  FROM `sqlite_master`\n  WHERE type='table';")
            const results = db.exec('SELECT * FROM senators')
            setResults(results)
        }
    }, [db])

    return (
        <div className="networkWrapper">
            <Table columns={resultsToColumnData(results)} data={resultsToData(results)}/>
        </div>
    )
}

export default Network