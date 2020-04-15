import React from 'react'

const withSQLite = (WrappedComponent) => {
    return class extends React.Component {
        render() {
            return (
                <div className="">
                    <WrappedComponent  {...this.props} />
                </div>
            )
        }
    }
}

export default withSQLite