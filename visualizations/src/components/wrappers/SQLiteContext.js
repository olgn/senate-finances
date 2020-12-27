import React, { createContext, useState, useLayoutEffect } from 'react'
import initSqlJs from 'sql.js'

const SQLiteContext = createContext(null)

const SQLiteContextProvider = ({ children }) => {
    const [db, setDb] = useState(null)
    const [err, setErr] = useState(null)

    useLayoutEffect(() => {
        initSqlJs()
            .then((SQL) =>
                fetch(`${process.env.PUBLIC_URL}/db.sqlite`)
                    .then((response) => response.arrayBuffer())
                    .then((buff) => {
                        const uInt8Array = new Uint8Array(buff)
                        setDb(new SQL.Database(uInt8Array))
                    })
            )
            .catch((err) => setErr(err))
    }, [])

    if (!db) return <pre>Loading...</pre>
    return (
        <SQLiteContext.Provider value={{ db, err }}>
            {children}
        </SQLiteContext.Provider>
    )
}

export { SQLiteContext }
export default SQLiteContextProvider
