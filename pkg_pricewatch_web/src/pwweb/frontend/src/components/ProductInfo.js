import React, { Component } from "react"

class ProjectInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: 'GERBER LIL’ CRUNCHIES, Mild Cheddar, Toddler Snacks | Walmart Canada',
      image: 'https://i5.walmartimages.ca/images/Large/109/7_2/999999-15000141097_2.jpg',
      description: 'Buy GERBER LIL’ CRUNCHIES, Mild Cheddar, Toddler Snacks from Walmart Canada. Shop for more Baby Snacks & Finger Foods  available online at Walmart.ca',
      price: 2.77,
      stock: 119,
    };
  }

  render() {
    return (
      <div className="card mb-3" style={{maxWidth: '100%'}}>
        <div className="row no-gutters">
          <div className="col-md-4">
            <img src={this.state.image} className="card-img" alt={this.state.title} />
          </div>
          <div className="col-md-8">
            <div className="card-body">
              <h5 className="card-title">{this.state.title}</h5>
              <p className="card-text">{this.state.description}</p>
              <p className="card-text"><small className="text-muted">${this.state.price}</small></p>
              <p className="card-text"><small className="text-muted">{this.state.stock}</small></p>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ProjectInfo;
