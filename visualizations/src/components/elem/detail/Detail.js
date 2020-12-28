import React from 'react'

export default ({title, data}) => {
    const rows = Object.keys(data).map((key, idx) => (
        <div className="field is-horizontal" key={idx}>
            <div className="field-label is-normal">
                <label className="label">{key}:</label>
            </div>
            <div className="field-body">
                <div className="field is-expanded">
                    <div className="control">{data[key]}</div>
                </div>
            </div>
        </div>
    ))
    return (
        <div className="detailWrapper">
            <h2 className="detailTitle">{title}</h2>
            <form className="form is-multiline detailContainer">
                {rows}
            </form>
        </div>
    )
}