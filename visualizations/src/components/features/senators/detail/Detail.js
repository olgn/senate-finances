import React, { useContext } from 'react'

import DataContextProvider, { DataContext } from './DataContext'
import Table from '../../../elem/table/Table'
import Detail from '../../../elem/detail/Detail'

const SenatorDetail = () => {
    const { columns, data, detailData } = useContext(DataContext)

    return (
        <>
            <Detail data={detailData} title={'Senator Info:'} />
            <Table columns={columns} data={data} title={'Senator Transactions'}/>
        </>
    )
}

export default () => (
    <DataContextProvider>
        <SenatorDetail />
    </DataContextProvider>
)
