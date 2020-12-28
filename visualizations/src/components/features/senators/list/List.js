import React, { useContext } from 'react'

import DataContextProvider, { DataContext } from './DataContext'
import Table from '../../../elem/table/Table'

const List = () => {
    const { columns, data } = useContext(DataContext)
    return <Table columns={columns} data={data} title={'Senators'}/>
}

export default () => (
    <DataContextProvider>
        <List />
    </DataContextProvider>
)
