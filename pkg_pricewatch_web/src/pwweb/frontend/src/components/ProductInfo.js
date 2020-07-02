import React, { Component } from "react"

class ProjectInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      product: props.product
    };
  }

  render() {
    return (
      <div className="card mb-3" style={{maxWidth: '100%'}}>
        <div className="row no-gutters">
          <div className="col-md-4">
            <img src={this.state.product.image} className="card-img" alt={this.state.product.title} />
          </div>
          <div className="col-md-8">
            <div className="float-right">
              <button type="button" className="close" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="card-body">
              <h5 className="card-title">{this.state.product.title}</h5>
              <p className="card-text">{this.state.product.description}</p>
              <p className="card-text"><small className="text-muted">${this.state.product.price}</small></p>
              <p className="card-text"><small className="text-muted">Qty. {this.state.product.stock}</small></p>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ProjectInfo;
