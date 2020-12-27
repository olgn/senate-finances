const resultsToData = (results) => {
    if (!results || !results.length) {
        return []
    }
    const { columns, values } = results[0]
    return values.map((value) => {
        return columns.reduce((acc, curr, idx) => {
            return {
                ...acc,
                [curr]: value[idx],
            }
        }, {})
    })
}

const resultsToColumnData = (results) => {
    if (!results || !results.length) {
        return []
    } else {
        const { columns } = results[0]
        return columns
    }
}

export { resultsToData, resultsToColumnData }
