import React, { Component } from "react"
import ProductInfo from "./ProductInfo.js"

class ProjectList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      products: props.products
    };
  }

  render() {
    return (
      <div>
        {this.props.products.map(product => <ProductInfo key={product.id} product={product} />)}
      </div>
    );
  }
}
  
export default ProjectList;
